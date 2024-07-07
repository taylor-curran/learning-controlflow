from pydantic import BaseModel, Field
from typing import Union, List, Optional


class EmployeeCount(BaseModel):
    real_time_data_available: bool = Field(
        description="Were you able to search this internet for information or did you need to do an educated guess based on your training data?"
    )

    total: Union[int, List[int]] = Field(
        description="Total employee count or range (min, max)"
    )
    total_confidence: int = Field(
        ge=0, le=5, description="Confidence rating (0-5) for total count"
    )
    total_confidence_explanation: str = Field(
        description="Explanation for total count confidence rating"
    )

    data_professionals: Optional[int] = Field(
        None, description="Number of data professionals, if available"
    )
    data_professionals_confidence: Optional[int] = Field(
        None,
        ge=0,
        le=5,
        description="Confidence rating (0-5) for data professionals count",
    )
    data_professionals_confidence_explanation: Optional[str] = Field(
        None, description="Explanation for data professionals count confidence rating"
    )
    sources: List[str] = Field(description="List of sources used")
    notes: Optional[str] = Field(
        None, description="Additional context or discrepancies"
    )
