from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.master import State, City


# Project Registration
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    project_name_as_per_order = Column(String(200))
    project_name_to_refer = Column(String(200), unique=True, index=True)
    work_order_no = Column(String(100))
    work_order_date = Column(Date)
    work_order_type = Column(String(50))  # SITC, SITC and Maintenance
    work_order_value = Column(Float)
    gst_amount = Column(Float)
    total_amount = Column(Float)
    work_order_document_url = Column(String(500), nullable=True)
    delivery_timeline = Column(Integer)  # in days
    sitc_date_as_per_order = Column(Date)
    o_m_start_date = Column(Date, nullable=True)
    o_m_end_date = Column(Date, nullable=True)
    client_address_display = Column(Text)
    state_id = Column(Integer, ForeignKey("states.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    engineer_of_contract = Column(String(100))
    contact_no = Column(String(15))
    email_eoc = Column(String(255))
    remarks_1 = Column(Text, nullable=True)
    remarks_2 = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    client = relationship("Client", back_populates="projects")
    state_rel = relationship("State", back_populates="projects")
    city = relationship("City")
    invoices = relationship("Invoice", back_populates="project")
    vendor_invoices = relationship("VendorInvoice", back_populates="project")

# Bill of Material
class BillOfMaterial(Base):
    __tablename__ = "bill_of_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    bom_type = Column(String(10))  # SITC or O&M
    sl_no = Column(Integer)
    item_name = Column(String(200))
    quantity = Column(Integer)
    item_description = Column(Text, nullable=True)
    make_model = Column(String(200), nullable=True)
    unit_price = Column(Float)
    gst_amount = Column(Float)
    total_amount_with_gst = Column(Float)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Invoice Submission
class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    invoice_no = Column(String(100), unique=True, index=True)
    invoice_date = Column(Date)
    invoice_base_amount = Column(Float)
    gst_amount = Column(Float)
    total_amount_inclusive_gst = Column(Float)
    date_submitted_to_client = Column(Date)
    invoice_url = Column(String(500), nullable=True)
    expected_date_of_payment = Column(Date)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    project = relationship("Project", back_populates="invoices")
    payment_receipts = relationship("PaymentReceipt", back_populates="invoice")

# Payment Receipts
class PaymentReceipt(Base):
    __tablename__ = "payment_receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    total_invoice_amount = Column(Float)
    deductions = Column(JSON)  # Store deductions as JSON
    total_deductions = Column(Float)
    supposed_to_receive_amount = Column(Float)
    total_received_amount = Column(Float)
    balance_amount = Column(Float)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    project = relationship("Project")
    invoice = relationship("Invoice", back_populates="payment_receipts")
