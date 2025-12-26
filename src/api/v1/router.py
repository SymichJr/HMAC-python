"""Module with routes"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.services.hmac_service import HMACSigner, get_hmac_service
from src.services.utils.validators import validate_content_type
from src.schamas.responce_schema import SignResponce, VerifyResponse
from src.schamas.verify_schema import SignRequest, VerifyRequest

from src.core.config import _config_instance
from src.core.log import logger, log_hmac_operation

router = APIRouter(prefix="/hmac_sign", tags=["hmac_sign"])


@router.post(
    "/sign",
    response_model=SignResponce,
    dependencies=[Depends(validate_content_type)],
    summary="Route to sign message",
)
async def sign_message(
    request: SignRequest,
    hmac_service: HMACSigner = Depends(get_hmac_service),
) -> SignResponce:
    """
    Sign handler.
    """
    msg_bytes = request.msg.encode("utf-8")
    msg_len = len(msg_bytes)

    if not request.msg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid_msg"
        )

    if msg_len > _config_instance.max_msg_size_bytes:
        log_hmac_operation(
            "SIGN",
            msg_len,
            "FAIL",
            details=(
                "413: max_msg_size_bytes exceeded "
                f"({_config_instance.max_msg_size_bytes})"
            ),
        )
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="payload_too_large",
        )

    try:
        signature = hmac_service.sign(request.msg)
        return SignResponce(signature=signature)

    except Exception as e:
        logger.error(
            f"Внутренняя ошибка при подписании сообщения: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal_error",
        )


@router.post(
    "/verify",
    response_model=VerifyResponse,
    dependencies=[Depends(validate_content_type)],
    summary="Route to verify message sign",
)
async def verify(
    request: VerifyRequest,
    hmac_service: HMACSigner = Depends(get_hmac_service),
) -> VerifyResponse:
    msg_bytes = request.msg.encode("utf-8")
    msg_len = len(msg_bytes)

    # Не понятно зачем, если pydantic и так может
    # валидировать, но ответ 400 есть в ТЗ
    # при отсутсвии подписи
    if not request.signature:
        log_hmac_operation(
            "VERIFY", msg_len, "FAIL", details="400: no signature provided"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no_signature_provided",
        )

    if not request.msg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid_msg"
        )

    if msg_len > _config_instance.max_msg_size_bytes:
        log_hmac_operation(
            "VERIFY",
            msg_len,
            "FAIL",
            details=(
                f"413: max_msg_size_bytes exceeded "
                f"({_config_instance.max_msg_size_bytes})"
            ),
        )
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="payload_too_large",
        )

    try:
        result = hmac_service.verify(
            msg=request.msg, signature=request.signature
        )
        return VerifyResponse(ok=result)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid_signature_format",
        )
    except Exception as e:
        logger.error(
            f"Внутренняя ошибка при подписании сообщения: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal_error",
        )
