from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


# Performance Appraisal Schemas
class PerformanceAppraisalBase(BaseModel):
    employee_id: int
    appraisal_date: date
    increment_amount: float
    promotion: bool = False
    increment_effective_date: date
    salary_after_increment: float
    performance_appraiser: str
    promoted_from_id: Optional[int] = None
    promoted_to_id: Optional[int] = None

class PerformanceAppraisalCreate(PerformanceAppraisalBase):
    pass

class PerformanceAppraisal(PerformanceAppraisalBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
