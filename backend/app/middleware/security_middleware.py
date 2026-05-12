from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import time
import re

from app.core.config import settings

limiter = Limiter(key_func=get_remote_address)


async def csrf_middleware(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        content_type = request.headers.get("content-type", "")
        if "multipart/form-data" not in content_type:
            origin = request.headers.get("origin", "")
            host = request.headers.get("host", "")
            if origin and host not in origin and "localhost" not in origin:
                return JSONResponse(status_code=403, content={"detail": "CSRF check failed"})
    response = await call_next(request)
    return response


async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response


def sanitize_input(value: str) -> str:
    if not isinstance(value, str):
        return value
    dangerous = re.compile(r"[\'\"\;\-\-\/\*\<\>\=\(\)]")
    return dangerous.sub("", value)


async def input_sanitization_middleware(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH"):
        if request.headers.get("content-type") == "application/json":
            body = await request.body()
            sanitized = sanitize_input(body.decode())
            request._body = sanitized.encode()
    return await call_next(request)
