from pydantic import BaseModel, Field
from typing import Union, List, Optional, Dict


class TotalEmployeeCount(BaseModel):
    company: str
    employee_count: int
    source: str


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


# too much info in the objectives and too confusing information in the data models
# use to get updated information -- write in the docstring of the function


class DataStack(BaseModel):
    tools: Dict[str, float] = Field(default_factory=dict)
    primary_languages: List[str] = Field(default_factory=list)
    sources: List[str] = Field(
        default_factory=list,
        description="Sources of the data professional count information",
    )
    notes: Optional[str] = None


class ICPScore(BaseModel):
    score: int = Field(..., ge=0, le=100)
    employee_factor: float = Field(..., ge=0, le=1)
    data_team_factor: float = Field(..., ge=0, le=1)
    tech_stack_factor: float = Field(..., ge=0, le=1)
    key_tools: List[str]
    explanation: str
    confidence: float = Field(..., ge=0, le=5)
