from pydantic import BaseModel


class SymptomOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

