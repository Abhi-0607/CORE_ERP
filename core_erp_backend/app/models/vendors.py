from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.master import State, City


# Vendor Registration
class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    contact_name = Column(String(100))
    contact_number_1 = Column(String(15))
    contact_number_2 = Column(String(15), nullable=True)
    designation = Column(String(100), nullable=True)
    address = Column(Text)
    state_id = Column(Integer, ForeignKey("states.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    email = Column(String(255))
    products = Column(JSON)  # Store products as JSON array
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    state_rel = relationship("State", back_populates="vendors")
    city_rel = relationship("City", back_populates="vendors")
    invoices = relationship("VendorInvoice", back_populates="vendor")

# Vendor Invoices
class VendorInvoice(Base):
    __tablename__ = "vendor_invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    invoice_amount = Column(Float)
    reference_project_name = Column(String(200))
    reference_client_invoice_no = Column(String(100))
    invoice_url = Column(String(500), nullable=True)
    purchase_order_url = Column(String(500), nullable=True)
    payment_terms = Column(Text, nullable=True)
    credit_period = Column(Integer, nullable=True)  # in days
    credit_period_start_date = Column(Date, nullable=True)
    credit_period_end_date = Column(Date, nullable=True)
    material_billed_description = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    vendor = relationship("Vendor", back_populates="invoices")
    project = relationship("Project", back_populates="vendor_invoices")
    payments = relationship("VendorPayment", back_populates="invoice")

# Vendor Payments
class VendorPayment(Base):
    __tablename__ = "vendor_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    invoice_id = Column(Integer, ForeignKey("vendor_invoices.id"))
    invoice_amount = Column(Float)
    balance_amount = Column(Float)
    purchase_order_url = Column(String(500), nullable=True)
    amount_paid = Column(Float)
    payment_date = Column(Date)
    transaction_details = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    vendor = relationship("Vendor")
    project = relationship("Project")
    invoice = relationship("VendorInvoice", back_populates="payments")