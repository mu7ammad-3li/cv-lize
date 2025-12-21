"""
Rate limiting middleware using slowapi
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"],  # Default rate limit
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Custom handler for rate limit exceeded errors
    """
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
            "retry_after": exc.detail,
        },
    )
