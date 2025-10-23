from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from app.settings.access_token import AccessToken

access_token = AccessToken().ACCESS_TOKEN


async def check_auth_token(request, call_next):
    """Check if the request has the correct Authorization: Bearer <token>"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing or invalid Authorization header"},
        )

    # Extract the token safely
    token = auth_header.removeprefix("Bearer ").strip()

    if token != access_token:
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid token"},
        )

    return await call_next(request)
