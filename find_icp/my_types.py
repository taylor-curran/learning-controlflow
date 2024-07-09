from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class TotalEmployeeCount(BaseModel):
    company: str = Field(default_factory=str, description="Name of the company")
    employee_count: int | None = Field(default=None, description="Total employee count")
    sources: List[str] = Field(
        default_factory=list, description="Sources of the employee count information"
    )
    notes: str | None = Field(
        default_factory=str, description="Additional notes about the employee count"
    )


class DataProfessionalCount(BaseModel):
    company: str = Field(default_factory=str, description="Name of the company")
    data_professional_count: int | None = Field(
        default=None, description="Total count of data professionals"
    )
    roles: Dict[str, int] = Field(
        default_factory=dict,
        description="Breakdown of data professional roles and their counts",
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Sources of the data professional count information",
    )
    notes: str | None = Field(
        default_factory=str,
        description="Additional notes about the data professional count",
    )


class DataStack(BaseModel):
    tools: List[str] = Field(
        default_factory=list,
        description="Key data tools and technologies used. Examples include: "
        "Python (data science), Databricks/Snowflake (data lake/warehouse), "
        "dbt (transformation), Kubernetes/Docker (containerization), "
        "Kafka (streaming), OpenAI GPT/Anthropic Claude/LLaMA/PaLM (AI/LLM), "
        "AWS/GCP/Azure (cloud)",
    )
    primary_languages: List[str] = Field(
        default_factory=list,
        description="Main programming languages used in the data stack (e.g., Python, SQL, Scala, R)",
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Sources of information for the data stack details",
    )
    notes: Optional[str] = Field(
        default_factory=str,
        description="Additional context or observations about the company's data technology stack",
    )


class ICPScore(BaseModel):
    score: Optional[int] = Field(
        default=None, ge=0, le=100, description="Overall ICP score from 0 to 100"
    )
    employee_factor: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Contribution of total employee count to the score",
    )
    data_team_factor: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Contribution of data professional count to the score",
    )
    tech_stack_factor: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Contribution of technology stack to the score",
    )
    key_tools: List[str] = Field(
        default_factory=list,
        description="Key tools identified in the tech stack that contributed to the score",
    )
    explanation: Optional[str] = Field(
        default=None, description="Detailed explanation of the score calculation"
    )
