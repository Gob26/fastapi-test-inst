from pydantic import BaseModel


class Inst(BaseModel):
    login: str
    password: str
    profile: str