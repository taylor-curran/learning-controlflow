import controlflow as cf
from pydantic import BaseModel

class DateStr(BaseModel):
    date: str

@cf.flow
def historical_events_flow():
    date_task = cf.Task("Get today's date", result_type=DateStr)
    dateHistory = cf.Task(
        "What happened on the date in history", 
        context=dict(date=date_task)
    )
    return dateHistory


result = historical_events_flow()
print(result)