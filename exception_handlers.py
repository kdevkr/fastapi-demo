import logging
import traceback

from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def exception_handler(request: Request, exc: Exception):
    # logging.error(traceback.format_exc())
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )


async def custom_http_exception_handler(request, exc: HTTPException):
    logging.error(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"OMG! The client sent invalid data!: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )