import pytest

from app.validator import SQLValidationError, validate_sql


def test_allows_select_query():
    sql = "SELECT department_name FROM departments;"
    assert validate_sql(sql) == sql


@pytest.mark.parametrize("keyword", ["DROP", "DELETE", "ALTER", "UPDATE", "TRUNCATE"])
def test_rejects_dangerous_keywords(keyword):
    with pytest.raises(SQLValidationError):
        validate_sql(f"{keyword} TABLE departments;")


def test_rejects_non_select_query():
    with pytest.raises(SQLValidationError):
        validate_sql("INSERT INTO departments VALUES (99, 'Test', 90);")
