from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from typing import Optional


security = HTTPBearer()


class AuthMiddleware:
    """
    JWT Authentication Middleware für FastAPI.
    Verifiziert Access Tokens und extrahiert User-Informationen.
    """

    def __init__(self):
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    def verify_token(self, token: str) -> dict:
        """
        Verifiziert JWT Token und gibt Payload zurück.

        Args:
            token: JWT Access Token

        Returns:
            dict mit user_id, email, role

        Raises:
            HTTPException: Wenn Token invalid oder expired
        """
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )

            # Token Type prüfen (muss access token sein)
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )

            return {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role")
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


# Dependency für FastAPI Routes
auth_middleware = AuthMiddleware()


def get_current_user(credentials: HTTPAuthorizationCredentials = security) -> dict:
    """
    FastAPI Dependency für geschützte Routes.
    Extrahiert und verifiziert JWT Token aus Authorization Header.

    Usage:
        @router.get("/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            user_id = current_user["user_id"]
            ...

    Returns:
        dict mit user_id, email, role

    Raises:
        HTTPException: Wenn Token fehlt oder invalid
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials"
        )

    token = credentials.credentials
    return auth_middleware.verify_token(token)


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = security
) -> Optional[dict]:
    """
    FastAPI Dependency für optional geschützte Routes.
    Gibt None zurück wenn kein Token vorhanden.

    Usage:
        @router.get("/maybe-protected")
        async def route(current_user: Optional[dict] = Depends(get_current_user_optional)):
            if current_user:
                # Authenticated
                user_id = current_user["user_id"]
            else:
                # Anonymous
                ...

    Returns:
        dict mit user_id, email, role oder None
    """
    if not credentials:
        return None

    token = credentials.credentials
    try:
        return auth_middleware.verify_token(token)
    except HTTPException:
        return None
