import configparser
import logging.config
from datetime import datetime

import sentry_sdk
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from exception_handlers import exception_handler, custom_http_exception_handler, validation_exception_handler
from scheduler import scheduler
from settings import settings

logger = logging.getLogger(__name__)
logging.config.fileConfig("conf/logging.conf", disable_existing_loggers=False)

# build-info.txt 파일 읽기
build_info = configparser.ConfigParser()
build_info.read("build-info.txt")

VERSION = build_info.get("build-info", "version", fallback="unknown")
BUILD_TIME = build_info.get("build-info", "build_time", fallback="unknown")

if settings.sentry_enable:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        enable_tracing=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

# Application
app = FastAPI(debug=settings.debug)
start_time = datetime.utcnow()

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

if settings.sentry_enable:
    app.add_middleware(SentryAsgiMiddleware)

# Global Exception Handler
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Register an event for application startup
@app.on_event("startup")
async def startup_event():
    logger.info("Startup application.")
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutdown application.")
    scheduler.shutdown()


# API
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    now = datetime.utcnow()
    uptime = now - start_time
    return {
        "timestamp": now.isoformat(),
        "version": VERSION,
        "build_time": BUILD_TIME,
        "start_time": start_time.isoformat(),
        "uptime": str(uptime)
    }


@app.get("/divide")
async def division_by_zero():
    result = 1 / 0
    return {"result": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
