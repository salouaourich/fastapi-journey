from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class AppointmentType(str, Enum):
 checkup = "checkup"
 emergency = "emergency"
 consultation = "consultation"


class Appointment(BaseModel):
 id: int
 doctor_name: str = Field(..., min_length=3)
 date: str
 type: AppointmentType


class Patient(BaseModel):
 id: int
 name: str = Field(..., min_length=3, max_length=50)
 age: int = Field(..., gt=0, lt=120)
 phone: Optional[str] = None
 appointments: List[Appointment] = []