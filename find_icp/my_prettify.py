from typing import Union, List, Optional
from pydantic import BaseModel, Field


def prettify(model: BaseModel) -> str:
    """
    Prettify the print output of a Pydantic model instance.

    Args:
        model (BaseModel): The Pydantic model instance.

    Returns:
        str: A prettified string representation of the model.
    """
    lines = []
    for field_name, field_value in model.dict().items():
        if isinstance(field_value, list):
            field_value = ", ".join(map(str, field_value))
        lines.append(f"{field_name.replace('_', ' ').title()}: {field_value}\n")

    return "\n".join(lines)


# Example usage
if __name__ == "__main__":

    class EmployeeCount(BaseModel):
        real_time_data_available: bool = Field(
            description="Whether real-time data was available for this research"
        )
        data_as_of: str = Field(
            description="The date of the most recent data used in this report"
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
            None,
            description="Explanation for data professionals count confidence rating",
        )

        industry_comparison: str = Field(
            description="Comparison to industry average (e.g., 'above average', 'average', 'below average')"
        )
        sources: List[str] = Field(description="List of sources used")
        notes: Optional[str] = Field(
            None, description="Additional context or discrepancies"
        )

    example = EmployeeCount(
        real_time_data_available=True,
        data_as_of="2023-07-06",
        total=[10000, 12000],
        total_confidence=4,
        total_confidence_explanation="Based on multiple reliable sources",
        data_professionals=200,
        data_professionals_confidence=3,
        data_professionals_confidence_explanation="Estimated based on LinkedIn profiles",
        industry_comparison="Above average",
        sources=["Source1", "Source2"],
        notes="Significant growth in the last year",
    )
    print(prettify(example))
