import controlflow as cf
from typing import Optional
from pydantic import BaseModel


class DateStr(BaseModel):
    date: str


date_task = cf.Task("Get today's date", result_type=DateStr)

dateHistory = cf.Task(
    "What happened on the date in history", context=dict(date=date_task)
)

dateHistory.run()
