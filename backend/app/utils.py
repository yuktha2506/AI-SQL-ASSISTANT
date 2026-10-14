import json
import logging
import re
from typing import Any

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def parse_json_response(raw_response: str) -> dict[str, Any]:
    cleaned = raw_response.strip()

    if not cleaned:
        raise ValueError("The AI response was empty.")

    fenced_match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if fenced_match:
        cleaned = fenced_match.group(1).strip()
    else:
        object_match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if object_match:
            cleaned = object_match.group(0).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError("The AI response was not valid JSON.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("The AI response must be a JSON object.")

    return parsed
