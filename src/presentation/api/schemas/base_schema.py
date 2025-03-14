from pydantic import BaseModel


class BaseSchema(BaseModel):
    detail: str
