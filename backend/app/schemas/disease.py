from pydantic import BaseModel


class DiseaseOut(BaseModel):
    id: int
    name: str
    type: str
    zoonotic: bool

    model_config = {"from_attributes": True}

