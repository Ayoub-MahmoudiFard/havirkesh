from pydantic import BaseModel as PydanticBase

class AISchema(PydanticBase):
    message: str
