from fastapi import FastAPI, HTTPException
from typing import List
import asyncio
from models import Patient

app = FastAPI()

patients: List[Patient] = []
@app.get("/patients/")
async def get_patients():
    await asyncio.sleep(1)
    return patients
@app.get("/patients/{id}")
async def get_patient(id: int):
    for patient in patients:
        if patient.id == id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")
@app.post("/patients/")
async def add_patient(patient: Patient):
    patients.append(patient)
    return patient
@app.put("/patients/{id}")
async def update_patient(id: int, updated_patient: Patient):
    for index, patient in enumerate(patients):
        if patient.id == id:
            patients[index] = updated_patient
            return updated_patient
    raise HTTPException(status_code=404, detail="Patient not found")
@app.delete("/patients/{id}")
async def delete_patient(id: int):
 for index, patient in enumerate(patients):
  if patient.id == id:
    del patients[index]
    return {"message": "Patient deleted"}
 raise HTTPException(status_code=404, detail="Patient not found")
