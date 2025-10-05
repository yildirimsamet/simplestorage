from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from typing import Union


async def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "success": False,
            "message": exception.detail,
            "data": None
        }
    )
