from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    hr_manager = "hr_manager"
    employee = "employee"


class LeaveStatusEnum(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="user", uselist=False)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    position = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="employee")
    department = relationship("Department", back_populates="employees")
    leave_requests = relationship("LeaveRequest", back_populates="employee")
    payrolls = relationship("Payroll", back_populates="employee")
    performance_reviews = relationship("PerformanceReview", back_populates="employee")


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type = Column(String, nullable=False)  # e.g. annual, sick, maternity
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(Enum(LeaveStatusEnum), default=LeaveStatusEnum.pending)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="leave_requests")


class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    basic_salary = Column(Float, nullable=False)
    bonus = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)
    net_salary = Column(Float, nullable=False)
    paid_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="payrolls")


class PerformanceReview(Base):
    __tablename__ = "performance_reviews"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    review_period = Column(String, nullable=False)  # e.g. "Q1 2026"
    rating = Column(Integer, nullable=False)  # 1-5
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="performance_reviews")
