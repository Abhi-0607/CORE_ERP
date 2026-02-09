from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Details
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    fathers_name = Column(String(100), nullable=True)
    photograph_url = Column(String(500), nullable=True)  # Store file path/URL
    
    # Date fields
    date_of_birth = Column(Date, nullable=True)
    date_of_joining = Column(Date, nullable=False)
    
    # Gender and Blood Group
    gender = Column(String(10), nullable=True)  # Male, Female, Other
    blood_group = Column(String(5), nullable=True)  # A+, B+, O+, etc.
    
    # Employee Details
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    work_location = Column(String(100), nullable=True)
    
    # Department and Designation (store as strings for now, can be foreign keys later)
    department = Column(String(100), nullable=True)  # Tech, Project Management, QA, Finance
    designation = Column(String(100), nullable=True)  # VP, AVP, Site Supervisor, etc.
    
    # Manager details
    is_manager = Column(Boolean, default=False)
    reporting_to = Column(Integer, nullable=True)  # ID of reporting manager
    
    # Contact Details
    mobile_number = Column(String(15), nullable=True)
    personal_email = Column(String(255), nullable=True)
    official_email = Column(String(255), nullable=False)
    emergency_mobile = Column(String(15), nullable=True)
    emergency_relation = Column(String(50), nullable=True)
    
    # Current Address
    current_address = Column(Text, nullable=True)
    current_state = Column(String(100), nullable=True)
    current_city = Column(String(100), nullable=True)
    
    # Permanent Address
    permanent_address = Column(Text, nullable=True)
    permanent_state = Column(String(100), nullable=True)
    permanent_city = Column(String(100), nullable=True)
    
    # Identity & Bank Details
    aadhar_number = Column(String(12), nullable=True, unique=True)
    aadhar_file_url = Column(String(500), nullable=True)
    pan_number = Column(String(10), nullable=True, unique=True)
    
    # Bank Details
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)
    ifsc_code = Column(String(11), nullable=True)
    pf_number = Column(String(50), nullable=True)
    esi_number = Column(String(50), nullable=True)
    
    # Qualification & Experience
    highest_qualification = Column(String(100), nullable=True)  # B Tech, M Tech, etc.
    other_qualification = Column(String(100), nullable=True)  # If "Other" is selected
    year_of_passing = Column(Date, nullable=True)  # Store as month/year
    total_experience = Column(Float, nullable=True)  # In years
    last_company = Column(String(200), nullable=True)
    resume_url = Column(String(500), nullable=True)
    
    # Salary
    salary_ctc = Column(Float, nullable=True)
    
    # Status
    status = Column(String(20), default="Active")  # Active, Inactive, Terminated
    date_of_relieving = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships (if needed later)
    # manager = relationship("Employee", remote_side=[id], backref="subordinates")