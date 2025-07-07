from pydantic import BaseModel

class ExistResponse(BaseModel):
    exist: bool
