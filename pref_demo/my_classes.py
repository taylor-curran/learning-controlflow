from pydantic import BaseModel

class SalesforceLead(BaseModel):
    name: str
    title: str
    company: str
    email: str
    phone: str
    lead_status: str
    lead_owner: str
    industry: str
    annual_revenue: int