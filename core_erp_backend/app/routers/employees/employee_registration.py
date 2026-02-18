from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from app.database import get_db
from app.schemas.employees.employee_registration import (
    EmployeeRegistrationCreate, 
    EmployeeRegistrationUpdate, 
    EmployeeRegistrationResponse,
    EmployeeRegistrationListResponse,
    Status
)
from app.crud.forms.employees.employee_registration import EmployeeRegistrationCRUD
from app.dependencies import get_current_user
from app.models.users import User
from app.constants.roles import UserRole
from app.utils.permissions import Permission


router = APIRouter(prefix="/employees", tags=["employee-registration"])
logger = logging.getLogger(__name__)

@router.get("/", response_model=EmployeeRegistrationListResponse)
def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department: Optional[str] = None,
    status: Optional[str] = None,
    is_manager: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        crud = EmployeeRegistrationCRUD(db)
        
        filters: Dict[str, Any] = {}
        if department:
            filters['department'] = department
        if status:
            filters['status'] = status
        if is_manager is not None:
            filters['is_manager'] = is_manager
        
        employees = crud.get_all(skip=skip, limit=limit, filters=filters, search=search)
        total = crud.get_count(filters=filters, search=search)
        
        return EmployeeRegistrationListResponse(
            employees=employees,
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            per_page=limit
        )
    
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch employees"
        )

@router.get("/{employee_id}", response_model=EmployeeRegistrationResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        crud = EmployeeRegistrationCRUD(db)
        employee = crud.get(employee_id)
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        return employee
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching employee {employee_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch employee"
        )

@router.post("/", response_model=EmployeeRegistrationResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee_data: EmployeeRegistrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        crud = EmployeeRegistrationCRUD(db)

        Permission.require_roles(current_user, [UserRole.ADMIN, UserRole.HR])

        employee = crud.create(employee_data)
        return employee

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{employee_id}", response_model=EmployeeRegistrationResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeRegistrationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        crud = EmployeeRegistrationCRUD(db)
        #user_role = current_user.role
        #if user_role not in ["admin", "hr"]:
          #  raise HTTPException(
              #  status_code=status.HTTP_403_FORBIDDEN,
              #  detail="Not authorized to update employees"
           # )
        
        employee = crud.update(employee_id, employee_data)
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        return employee
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating employee {employee_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update employee"
        )

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        crud = EmployeeRegistrationCRUD(db)
        Permission.require_roles(current_user, [UserRole.ADMIN, UserRole.HR])
        
        success = crud.delete(employee_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting employee {employee_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete employee"
        )

@router.post("/{employee_id}/send-invite", status_code=status.HTTP_200_OK)
def send_employee_invite(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    Permission.require_roles(current_user, [UserRole.ADMIN, UserRole.HR])

    crud = EmployeeRegistrationCRUD(db)
    employee = crud.get(employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    # If already sent, don't resend unless you want to allow it
    if employee.invite_sent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invite already sent"
        )

    # TODO: later we will actually send email here
    # For now just mark as sent.
    employee.invite_sent = True
    employee.invite_sent_at = datetime.utcnow()

    db.commit()
    db.refresh(employee)

    return {
        "message": "Invite marked as sent",
        "employee_id": employee.id,
        "invite_sent": employee.invite_sent,
        "invite_sent_at": employee.invite_sent_at
    }
