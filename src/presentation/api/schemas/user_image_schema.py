from pydantic import BaseModel


class UserImageSchema(BaseModel):
    id: int
    image_path: str