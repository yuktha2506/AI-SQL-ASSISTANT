import logging
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import get_settings
from app.prompt import SYSTEM_PROMPT
from app.utils import parse_json_response
from app.validator import validate_sql


logger = logging.getLogger(__name__)

GEMINI_FALLBACK_MODELS = (
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
)

LOCAL_SQL_FALLBACKS: tuple[tuple[tuple[str, ...], dict[str, str]], ...] = (
    (
        ("top", "department", "placement"),
        {
            "sql": (
                "SELECT department_name, placement_percentage\n"
                "FROM departments\n"
                "ORDER BY placement_percentage DESC\n"
                "LIMIT 5;"
            ),
            "explanation": (
                "This query returns the five departments with the highest placement percentages."
            ),
        },
    ),
    (
        ("placement", "above"),
        {
            "sql": (
                "SELECT department_name, placement_percentage\n"
                "FROM departments\n"
                "WHERE placement_percentage > 85\n"
                "ORDER BY placement_percentage DESC;"
            ),
            "explanation": (
                "This query lists departments whose placement percentage is above 85, sorted highest first."
            ),
        },
    ),
    (
        ("cgpa", "greater"),
        {
            "sql": (
                "SELECT student_name, cgpa\n"
                "FROM students\n"
                "WHERE cgpa > 9\n"
                "ORDER BY cgpa DESC;"
            ),
            "explanation": (
                "This query lists students with CGPA greater than 9, sorted from highest CGPA to lowest."
            ),
        },
    ),
    (
        ("average", "marks", "course"),
        {
            "sql": (
                "SELECT c.course_name, ROUND(AVG(e.marks), 2) AS average_marks\n"
                "FROM courses c\n"
                "JOIN enrollments e ON c.course_id = e.course_id\n"
                "GROUP BY c.course_id, c.course_name\n"
                "ORDER BY average_marks DESC;"
            ),
            "explanation": (
                "This query calculates the average marks for each course using enrollments."
            ),
        },
    ),
    (
        ("courses", "computer science"),
        {
            "sql": (
                "SELECT c.course_name\n"
                "FROM courses c\n"
                "JOIN departments d ON c.department_id = d.department_id\n"
                "WHERE LOWER(d.department_name) = 'computer science'\n"
                "ORDER BY c.course_name;"
            ),
            "explanation": (
                "This query lists courses that belong to the Computer Science department."
            ),
        },
    ),
)


class SQLGenerator:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _build_llm(self, model_name: str | None = None):
        provider = self.settings.ai_provider.lower().strip()

        if provider == "gemini":
            if not self.settings.google_api_key:
                raise RuntimeError("GOOGLE_API_KEY is not configured.")

            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model=model_name or self.settings.gemini_model,
                google_api_key=self.settings.google_api_key,
            )

        if provider == "openai":
            if not self.settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY is not configured.")

            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=self.settings.openai_model,
                api_key=self.settings.openai_api_key,
                temperature=0,
            )

        raise RuntimeError(
            "Invalid AI_PROVIDER. Use 'gemini' or 'openai'."
        )

    def _candidate_models(self) -> list[str | None]:
        provider = self.settings.ai_provider.lower().strip()
        if provider != "gemini":
            return [None]

        candidates = [self.settings.gemini_model, *GEMINI_FALLBACK_MODELS]
        return list(dict.fromkeys(candidates))

    @staticmethod
    def _is_model_unavailable_error(error: Exception) -> bool:
        message = str(error).lower()
        return (
            "not found" in message
            or "no longer available" in message
            or "not available" in message
        )

    @staticmethod
    def _local_fallback(question: str) -> dict[str, str]:
        normalized_question = question.lower()

        for required_terms, result in LOCAL_SQL_FALLBACKS:
            if all(term in normalized_question for term in required_terms):
                return result

        return {
            "sql": "",
            "explanation": (
                "The question could not be converted locally. Please rephrase using the available "
                "tables: departments, students, courses, and enrollments."
            ),
        }

    @staticmethod
    def _response_text(response) -> str:
        if hasattr(response, "text") and response.text:
            return str(response.text)

        content = response.content
        if isinstance(content, list):
            return "".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
            )

        return str(content)

    async def generate(self, question: str) -> dict[str, str]:
        response = None
        last_error: Exception | None = None

        for model_name in self._candidate_models():
            llm = self._build_llm(model_name)

            try:
                logger.info(
                    "Generating SQL with %s%s for question: %s",
                    self.settings.ai_provider,
                    f" ({model_name})" if model_name else "",
                    question,
                )
                response = await llm.ainvoke(
                    [
                        SystemMessage(content=SYSTEM_PROMPT),
                        HumanMessage(content=question),
                    ]
                )
                break
            except Exception as exc:
                last_error = exc
                if self.settings.ai_provider.lower().strip() == "gemini" and self._is_model_unavailable_error(exc):
                    logger.warning("Gemini model unavailable, trying fallback: %s", exc)
                    continue
                raise

        if response is None:
            raise RuntimeError(
                "No configured Gemini model is available. Update GEMINI_MODEL to a current Gemini model."
            ) from last_error

        raw_response = self._response_text(response)
        try:
            parsed = parse_json_response(raw_response)
        except ValueError:
            logger.warning("AI returned invalid JSON. Using local fallback. Raw response: %r", raw_response)
            parsed = self._local_fallback(question)

        sql = validate_sql(str(parsed.get("sql", "")))
        explanation = str(parsed.get("explanation", "")).strip()

        if sql and not explanation:
            explanation = "This SQL query answers the requested question using the SQLite schema."

        return {
            "sql": sql,
            "explanation": explanation or "The question cannot be answered from the available schema.",
        }
