from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    name: str
    age: int


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int

    # ✅ NEW Pydantic V2 तरीका
    model_config = ConfigDict(from_attributes=True)