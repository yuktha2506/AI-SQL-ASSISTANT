import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas import GenerateSQLRequest, GenerateSQLResponse
from app.sql_generator import SQLGenerator
from app.validator import SQLValidationError


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=GenerateSQLResponse)
async def generate_sql(payload: GenerateSQLRequest) -> GenerateSQLResponse:
    generator = SQLGenerator()

    try:
        result = await generator.generate(payload.question)
    except SQLValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected SQL generation failure")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate SQL at this time.",
        ) from exc

    return GenerateSQLResponse(**result)
