from typing import Optional, Any

from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    status: str
    details: Optional[str] = None
    data: Optional[Any] = None

    class Config:
        from_attributes = True
