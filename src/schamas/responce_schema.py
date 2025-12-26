from pydantic import BaseModel


class SignResponce(BaseModel):
    """Model for /sign response"""

    signature: str


class VerifyResponse(BaseModel):
    """Model for /verify response"""

    ok: bool
