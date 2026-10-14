import re
from app.config import get_settings

DANGEROUS_SQL_KEYWORDS = ("DROP", "DELETE", "ALTER", "UPDATE", "TRUNCATE")


class SQLValidationError(ValueError):
    pass


def validate_sql(sql: str) -> str:
    normalized_sql = sql.strip()
    if not normalized_sql:
        return normalized_sql

    settings = get_settings()
    if settings.allow_dangerous_sql:
        return normalized_sql

    for keyword in DANGEROUS_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", normalized_sql, flags=re.IGNORECASE):
            raise SQLValidationError(
                f"Dangerous SQL keyword '{keyword}' is not allowed."
            )

    if not re.match(r"^\s*(SELECT|WITH)\b", normalized_sql, flags=re.IGNORECASE):
        raise SQLValidationError("Only SELECT or WITH queries are allowed.")

    return normalized_sql
