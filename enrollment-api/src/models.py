from pydantic import BaseModel


class Enrollment(BaseModel):
    CPF: str
    name: str
    age: int
