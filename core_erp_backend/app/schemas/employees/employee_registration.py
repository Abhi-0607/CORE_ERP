from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

# Enums
class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"

class Department(str, Enum):
    TECH = "Tech"
    PROJECT_MANAGEMENT = "Project Management"
    QA = "QA"
    FINANCE = "Finance"

class Designation(str, Enum):
    VP = "VP"
    AVP = "AVP"
    SITE_SUPERVISOR = "Site Supervisor"
    PROJECT_MANAGER = "Project Manager"
    SR_PROJECT_MANAGER = "Sr. Project Manager"
    SR_PROJECT_EXECUTIVE = "Sr. Project Executive"

class Status(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    TERMINATED = "Terminated"

# Base schema
class EmployeeRegistrationBase(BaseModel):
    # Personal Details
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    fathers_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    
    # Employee Details
    employee_id: str
    date_of_joining: date
    work_location: Optional[str] = None
    department: Optional[Department] = None
    designation: Optional[Designation] = None
    is_manager: bool = False
    reporting_to: Optional[int] = None
    official_email: EmailStr
    
    # Contact Details
    mobile_number: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    emergency_mobile: Optional[str] = None
    emergency_relation: Optional[str] = None
    
    # Address
    current_address: Optional[str] = None
    current_state: Optional[str] = None
    current_city: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_state: Optional[str] = None
    permanent_city: Optional[str] = None
    
    # Identity & Bank
    aadhar_number: Optional[str] = None
    pan_number: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    pf_number: Optional[str] = None
    esi_number: Optional[str] = None
    
    # Qualification & Experience
    highest_qualification: Optional[str] = None
    other_qualification: Optional[str] = None
    year_of_passing: Optional[date] = None
    total_experience: Optional[float] = None
    last_company: Optional[str] = None
    
    # Salary
    salary_ctc: Optional[float] = None
    
    # Status
    status: Status = Status.ACTIVE
    
    # Validators
    @validator('official_email')
    def official_email_must_be_company(cls, v):
        if not v.endswith("@coresonant.com"):
            raise ValueError('Official email must end with @coresonant.com')
        return v
    
    @validator('aadhar_number')
    def validate_aadhar(cls, v):
        if v and (len(v) != 12 or not v.isdigit()):
            raise ValueError('Aadhar number must be 12 digits')
        return v
    
    @validator('pan_number')
    def validate_pan(cls, v):
        if v and len(v) != 10:
            raise ValueError('PAN number must be 10 characters')
        return v
    
    @validator('mobile_number', 'emergency_mobile')
    def validate_phone(cls, v):
        if v and (len(v) != 10 or not v.isdigit()):
            raise ValueError('Mobile number must be 10 digits')
        return v

# Schema for creating employee
class EmployeeRegistrationCreate(EmployeeRegistrationBase):
    photograph_url: Optional[str] = None
    aadhar_file_url: Optional[str] = None
    resume_url: Optional[str] = None
    date_of_relieving: Optional[date] = None

# Schema for updating employee
class EmployeeRegistrationUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    work_location: Optional[str] = None
    department: Optional[Department] = None
    designation: Optional[Designation] = None
    is_manager: Optional[bool] = None
    reporting_to: Optional[int] = None
    official_email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    emergency_mobile: Optional[str] = None
    emergency_relation: Optional[str] = None
    current_address: Optional[str] = None
    current_state: Optional[str] = None
    current_city: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_state: Optional[str] = None
    permanent_city: Optional[str] = None
    aadhar_number: Optional[str] = None
    pan_number: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    pf_number: Optional[str] = None
    esi_number: Optional[str] = None
    highest_qualification: Optional[str] = None
    other_qualification: Optional[str] = None
    year_of_passing: Optional[date] = None
    total_experience: Optional[float] = None
    last_company: Optional[str] = None
    salary_ctc: Optional[float] = None
    status: Optional[Status] = None
    date_of_relieving: Optional[date] = None
    photograph_url: Optional[str] = None
    aadhar_file_url: Optional[str] = None
    resume_url: Optional[str] = None

# Schema for response
class EmployeeRegistrationResponse(EmployeeRegistrationBase):
    id: int
    photograph_url: Optional[str]
    aadhar_file_url: Optional[str]
    resume_url: Optional[str]
    date_of_relieving: Optional[date]
    invite_sent: bool
    invite_sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Schema for list response
class EmployeeRegistrationListResponse(BaseModel):
    employees: List[EmployeeRegistrationResponse]
    total: int
    page: int
    per_page: int