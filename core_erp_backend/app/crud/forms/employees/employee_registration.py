import string
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import logging

from app.models.employees.employee_registration import Employee
from app.schemas.employees.employee_registration import EmployeeRegistrationCreate, EmployeeRegistrationUpdate
from app.models.users import User

logger = logging.getLogger(__name__)

class EmployeeRegistrationCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
    
    def get_by_employee_id(self, emp_id: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.employee_id == emp_id).first()
    
    def get_by_email(self, email: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.official_email == email).first()
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None
    ) -> List[Employee]:
        query = self.db.query(Employee)
        
        if filters:
            for key, value in filters.items():
                if hasattr(Employee, key) and value is not None:
                    query = query.filter(getattr(Employee, key) == value)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Employee.first_name.ilike(search_term),
                    Employee.last_name.ilike(search_term),
                    Employee.employee_id.ilike(search_term),
                    Employee.official_email.ilike(search_term),
                )
            )
        
        query = query.order_by(Employee.created_at.desc())
        return query.offset(skip).limit(limit).all()
    
    def get_count(
        self,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None
    ) -> int:
        query = self.db.query(Employee)
        
        if filters:
            for key, value in filters.items():
                if hasattr(Employee, key) and value is not None:
                    query = query.filter(getattr(Employee, key) == value)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Employee.first_name.ilike(search_term),
                    Employee.last_name.ilike(search_term),
                    Employee.employee_id.ilike(search_term),
                    Employee.official_email.ilike(search_term),
                )
            )
        
        return query.count()
    
    def create(self, employee_data: EmployeeRegistrationCreate) -> Employee:
        existing = self.get_by_employee_id(employee_data.employee_id)
        if existing:
            raise ValueError(f"Employee ID {employee_data.employee_id} already exists")
        
        existing_email = self.get_by_email(employee_data.official_email)
        if existing_email:
            raise ValueError(f"Email {employee_data.official_email} already exists")
        
        db_employee = Employee(**employee_data.dict())
        
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)

        # NOTE: we are doing it here so it happens automatically.

        from app.models.users import User
        from app.utils.security import hash_password
        import secrets
        import string

        # Generate a random password (temporary)
        alphabet = string.ascii_letters + string.digits
        raw_password = "".join(secrets.choice(alphabet) for _ in range(10))

        # Check if user already exists with same email
        existing_user = self.db.query(User).filter(User.email == employee_data.official_email).first()
        if existing_user:
        # If employee exists but user already exists, we won't block for now.
        # But in real ERP, you may want to raise error.
            logger.warning(f"User already exists for email: {employee_data.official_email}")
        else:
            new_user = User(
                email=employee_data.official_email,
                role="EMPLOYEE",  # must match role
                hashed_password = hash_password(raw_password),
                is_active=True
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            # For now we just print password in console
            # Later you will email this password.
            print("\n=== EMPLOYEE USER CREATED ===")
            print(f"Employee: {db_employee.employee_id}")
            print(f"User Email: {new_user.email}")
            print(f"Temp Password: {raw_password}")
            print("=============================\n")

        logger.info(f"Created employee: {db_employee.employee_id} - {db_employee.first_name} {db_employee.last_name}")
        return db_employee

    
    def update(self, employee_id: int, employee_data: EmployeeRegistrationUpdate) -> Optional[Employee]:
        employee = self.get(employee_id)
        if not employee:
            return None
        
        update_data = employee_data.dict(exclude_unset=True)
        
        if 'employee_id' in update_data and update_data['employee_id'] != employee.employee_id:
            existing = self.get_by_employee_id(update_data['employee_id'])
            if existing:
                raise ValueError(f"Employee ID {update_data['employee_id']} already exists")
        
        if 'official_email' in update_data and update_data['official_email'] != employee.official_email:
            existing_email = self.get_by_email(update_data['official_email'])
            if existing_email:
                raise ValueError(f"Email {update_data['official_email']} already exists")
        
        for field, value in update_data.items():
            setattr(employee, field, value)
        
        employee.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(employee)
        
        logger.info(f"Updated employee ID {employee_id}")
        return employee
    
    def delete(self, employee_id: int) -> bool:
        employee = self.get(employee_id)
        if not employee:
            return False
        
        self.db.delete(employee)
        self.db.commit()
        logger.info(f"Deleted employee ID {employee_id}")
        return True
    
    def get_managers(self) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.is_manager == True).all()
    
    def get_by_department(self, department: str) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.department == department).all()
    
    def get_active_employees(self) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.status == "Active").all()