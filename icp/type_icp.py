from pydantic import BaseModel, Field
import controlflow as cf
from typing import Union, List, Optional
from prettify_my_stuff import pretty_print_employee_count

class EmployeeCount(BaseModel):
    real_time_data_available: bool = Field(description="Whether real-time data was available for this research")
    data_as_of: str = Field(description="The date of the most recent data used in this report")

    total: Union[int, List[int]] = Field(description="Total employee count or range (min, max)")
    total_confidence: int = Field(ge=0, le=5, description="Confidence rating (0-5) for total count")
    total_confidence_explanation: str = Field(description="Explanation for total count confidence rating")

    data_professionals: Optional[int] = Field(None, description="Number of data professionals, if available")
    data_professionals_confidence: Optional[int] = Field(None, ge=0, le=5, description="Confidence rating (0-5) for data professionals count")
    data_professionals_confidence_explanation: Optional[str] = Field(None, description="Explanation for data professionals count confidence rating")

    growth_rate: Optional[float] = Field(None, description="Annual growth rate as a percentage")
    growth_rate_confidence: Optional[int] = Field(None, ge=0, le=5, description="Confidence rating (0-5) for growth rate")
    growth_rate_confidence_explanation: Optional[str] = Field(None, description="Explanation for growth rate confidence rating")

    industry_comparison: str = Field(description="Comparison to industry average (e.g., 'above average', 'average', 'below average')")
    sources: List[str] = Field(description="List of sources used")
    notes: Optional[str] = Field(None, description="Additional context or discrepancies")

researcher = cf.Agent(
    "Researcher",
    instructions=f"""
    As a specialized company research agent, your responsibilities include:
    1. Cross-reference all findings with 1-2 additional sources.
    2. Make educated guesses when reliable sources are scarce, based on available info or company category.
    3. Prioritize the most recent data in all analyses.
    4. Cite sources and dates for all key findings, ensuring traceability.
    5. Rate confidence on a 0-5 scale for each key piece of information:
       5: Multiple corroborating sources with near-identical information
       4: Strong agreement among sources with minor variations
       3: Moderate confidence, some conflicting information
       2: Low confidence, significant data gaps or conflicts
       1: Very low confidence, mostly educated guesses
       0: Complete uncertainty, speculation based on tangential information
    6. Provide brief explanations for each confidence rating.
    7. Balance brevity with essential details in responses.
    8. Clearly differentiate between factual data and educated guesses.
    9. Highlight significant discrepancies between sources.
    10. Adapt research approach based on company size, industry, and public/private status.
    11. Consider recent news, market trends, and industry benchmarks in your analysis.
    12. Note any potential biases or limitations in the data sources used.
    13. Always check for the availability of real-time search tools before starting your research.
    14. If real-time search tools are unavailable, clearly state this limitation and significantly lower your confidence ratings.
    15. Remember that your training data has a cutoff date, and you should factor this into your confidence ratings when real-time data is unavailable.
    16. In the absence of real-time data, clearly state that your information might be outdated and provide the approximate date of your most recent reliable data.
    """
)

@cf.flow
def generate_icp_report(customer: str):
    number_of_employees = cf.Task(
        f"""Research and report on {customer}'s employee count:
        - Determine current total employee count (or estimate a range)
        - If possible, identify the number of data professionals
        - Assess recent growth trajectory (annual growth rate)
        - Compare to industry averages
        - Provide confidence ratings (0-5) with brief explanations for total count, data professionals count, and growth rate
        - Note any significant events or discrepancies
        - Provide all available information in the required format.
        - Before starting your research, explicitly check if you have access to real-time search tools.
        - If real-time search tools are unavailable, clearly state this limitation in your report and adjust your confidence ratings accordingly.
        - Provide the approximate date of your most recent reliable data when real-time data is unavailable.
        - Remember that your training data has a cutoff date, and factor this into your confidence ratings.
        
        """,
        agents=[researcher],
        result_type=EmployeeCount,
        instructions="""Provide the most accurate information possible. If real-time data is unavailable, use recent estimates or industry standards, clearly stating limitations in the notes field."""
    )
    
    result = number_of_employees.run()
    if result is None:
        print(f"Failed to gather information for {customer}. No data available.")
    else:
        pretty_print_employee_count(result)

if __name__ == "__main__":
    generate_icp_report("Blackstone")