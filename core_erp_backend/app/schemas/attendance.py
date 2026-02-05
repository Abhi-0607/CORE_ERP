from typing import Any, Dict, Optional
from typing import Any
from pydantic import BaseModel
from datetime import datetime

# Attendance Schemas

class AttendanceBase(BaseModel):
    employee_id: int
    year: int
    month: int
    attendance_data: Dict[str, Any]
    loss_of_pay: int = 0

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
