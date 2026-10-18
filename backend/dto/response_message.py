from pydantic import BaseModel


class ResponseMessage(BaseModel):
    status: int
    message: str

    model_config = {"from_attributes": True}
