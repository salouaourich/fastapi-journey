from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain", "experience": 10, "specialty": "Leadership"},
    {"id": 2, "name": "Alice", "role": "Engineer", "experience": 8, "specialty": "Mechanical"},
    {"id": 3, "name": "Bob", "role": "Scientist", "experience": 5, "specialty": "Biology"}
]


class CrewMember(BaseModel):
    name: str
    role: str
    experience: int
    specialty: str


@app.post("/crew")
def add_crew_member(member: CrewMember):

    new_member = {
        "id": len(crew) + 1,
        "name": member.name,
        "role": member.role,
        "experience": member.experience,
        "specialty": member.specialty
    }

    crew.append(new_member)

    return {
        "message": "Crew member added successfully",
        "crew_member": new_member
    }