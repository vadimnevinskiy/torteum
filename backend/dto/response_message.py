from pydantic import BaseModel


class ResponseMessage(BaseModel):
    status: int
    message: str
