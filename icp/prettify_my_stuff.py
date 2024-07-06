from typing import Union, List, Optional


def pretty_print_employee_count(result):
    def format_value(value: Union[int, List[int], float, str, None]) -> str:
        if isinstance(value, list):
            return f"{value[0]} - {value[1]}"
        elif value is None:
            return "N/A"
        else:
            return str(value)

    print("\n=== Employee Count Report ===")
    print(
        f"Real-time data available: {'Yes' if result.real_time_data_available else 'No'}"
    )
    print(f"Data as of: {result.data_as_of}")

    print(f"\nTotal Employees: {format_value(result.total)}")
    print(f"Confidence: {result.total_confidence}/5")
    print(f"Explanation: {result.total_confidence_explanation}")

    print(f"\nData Professionals: {format_value(result.data_professionals)}")
    if result.data_professionals is not None:
        print(f"Confidence: {result.data_professionals_confidence}/5")
        print(f"Explanation: {result.data_professionals_confidence_explanation}")

    print(f"\nGrowth Rate: {format_value(result.growth_rate)}%")
    if result.growth_rate is not None:
        print(f"Confidence: {result.growth_rate_confidence}/5")
        print(f"Explanation: {result.growth_rate_confidence_explanation}")

    print(f"\nIndustry Comparison: {result.industry_comparison}")

    print("\nSources:")
    for source in result.sources:
        print(f"- {source}")

    if result.notes:
        print(f"\nAdditional Notes: {result.notes}")

    print("============================")
