from pydantic import BaseModel, Field

class GenerateSQLRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)


class GenerateSQLResponse(BaseModel):
    sql: str
    explanation: str


class ErrorResponse(BaseModel):
    detail: str
