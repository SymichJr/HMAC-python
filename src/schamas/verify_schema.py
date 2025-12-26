from pydantic import BaseModel


class SignRequest(BaseModel):
    """Model for /sign request"""

    msg: str


class VerifyRequest(BaseModel):
    """Model for /verify request"""

    msg: str
    # | None = None для реализации ошибки 400 из ТЗ
    # По правильному должно быть signature: str
    signature: str | None = None
