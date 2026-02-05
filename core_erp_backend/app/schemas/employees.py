from pydantic import BaseModel, EmailStr, Field, validator, Status
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum

# Employee Schemas
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    fathers_name: Optional[str] = None
    date_of_joining: date
    employee_id: str
    mobile_no: str
    personal_email: EmailStr
    date_of_birth: date
    gender: str
    address: str
    aadhar_no: str
    status: Status = Status.ACTIVE
    salary_ctc: float
    
    # Foreign keys
    department_id: int
    designation_id: int
    city_id: int
    state_id: int
    working_location_id: int

class EmployeeCreate(EmployeeBase):
    photograph_url: Optional[str] = None
    current_location: Optional[str] = None
    aadhar_url: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_relation: Optional[str] = None
    blood_group_id: Optional[int] = None
    date_of_relieving: Optional[date] = None
    permanent_address: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_no: Optional[str] = None
    account_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_no: Optional[str] = None
    pf_no: Optional[str] = None
    esi_no: Optional[str] = None
    resume_url: Optional[str] = None
    qualification_id: Optional[int] = None
    year_of_passing: Optional[date] = None
    total_experience: Optional[float] = None
    last_company: Optional[str] = None

class EmployeeUpdate(BaseModel):
    status: Optional[Status] = None
    designation_id: Optional[int] = None
    salary_ctc: Optional[float] = None
    # Add other updatable fields

class Employee(EmployeeBase):
    id: int
    photograph_url: Optional[str]
    current_location: Optional[str]
    aadhar_url: Optional[str]
    emergency_contact: Optional[str]
    emergency_relation: Optional[str]
    date_of_relieving: Optional[date]
    permanent_address: Optional[str]
    bank_name: Optional[str]
    bank_account_no: Optional[str]
    account_name: Optional[str]
    ifsc_code: Optional[str]
    pan_no: Optional[str]
    pf_no: Optional[str]
    esi_no: Optional[str]
    resume_url: Optional[str]
    year_of_passing: Optional[date]
    total_experience: Optional[float]
    last_company: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]