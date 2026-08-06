import logging
from pathlib import Path

from sqlalchemy import text

from app import models  # noqa: F401
from app.config import BASE_DIR, DATABASE_PATH
from app.database import Base, SessionLocal, engine


logger = logging.getLogger(__name__)
SQL_DIR = BASE_DIR / "sql"


def _execute_sql_file(path: Path) -> None:
    if not path.exists():
        logger.warning("SQL file not found: %s", path)
        return

    statements = [statement.strip() for statement in path.read_text().split(";")]
    with engine.begin() as connection:
        for statement in statements:
            if statement:
                connection.execute(text(statement))


def _has_sample_data() -> bool:
    with SessionLocal() as session:
        result = session.execute(text("SELECT COUNT(*) FROM departments"))
        return int(result.scalar_one()) > 0


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)

    if not _has_sample_data():
        logger.info("Seeding SQLite database with sample data")
        _execute_sql_file(SQL_DIR / "sample_data.sql")
    else:
        logger.info("SQLite database already contains sample data")
