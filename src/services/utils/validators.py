from fastapi import HTTPException, Header, status
from typing import Annotated, Optional


async def validate_content_type(
    content_type: Annotated[Optional[str], Header()] = None,
):
    if content_type != "application/json":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported Media Type. Only application/json is allowed.",
        )
