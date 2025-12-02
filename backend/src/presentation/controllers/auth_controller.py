from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from ...application.dto.auth_dto import (
    RegisterRequestDTO,
    LoginRequestDTO,
    RegisterResponseDTO,
    LoginResponseDTO,
    UserResponseDTO
)
from ...application.use_cases.register_user_use_case import RegisterUserUseCase
from ...application.use_cases.login_user_use_case import LoginUserUseCase
from ..middlewares import get_current_user
from ..dependencies import get_register_user_use_case, get_login_user_use_case


router = APIRouter(prefix="/api/auth", tags=["auth"])


# ============== Request Models ==============

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============== Endpoints ==============

@router.post("/register", response_model=RegisterResponseDTO)
async def register(
    request: RegisterRequest,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case)
):
    """
    Registriert neuen User mit FREE Subscription.

    Returns:
    - User Details
    - JWT Tokens (Access & Refresh)
    - Automatisch erstellte FREE Subscription

    Errors:
    - 400: Email bereits registriert oder Validierung fehlgeschlagen
    - 500: Server Error
    """
    try:
        dto = RegisterRequestDTO(
            email=request.email,
            name=request.name,
            password=request.password
        )
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei Registrierung: {str(e)}"
        )


@router.post("/login", response_model=LoginResponseDTO)
async def login(
    request: LoginRequest,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case)
):
    """
    Loggt User ein und gibt JWT Tokens zurück.

    Returns:
    - User Details
    - JWT Tokens (Access & Refresh)

    Errors:
    - 401: Email oder Password falsch
    - 403: User Account deaktiviert
    - 500: Server Error
    """
    try:
        dto = LoginRequestDTO(
            email=request.email,
            password=request.password
        )
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Login: {str(e)}"
        )


@router.get("/me", response_model=UserResponseDTO)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """
    Gibt Informationen über den aktuell eingeloggten User zurück.

    Requires: Authentication (JWT Token)

    Returns:
    - User Details (id, email, name, role, subscription_id, etc.)

    Errors:
    - 401: Token fehlt oder invalid
    """
    # In production würde man den User aus der DB laden
    # Für jetzt: Return user info aus Token
    return UserResponseDTO(
        id=current_user["user_id"],
        email=current_user["email"],
        name="",  # Würde aus DB geladen
        role=current_user["role"],
        subscription_id=None,  # Würde aus DB geladen
        stripe_customer_id=None,
        is_active=True,
        created_at=None  # Würde aus DB geladen
    )


# TODO: Implement refresh token endpoint
# @router.post("/refresh", response_model=RefreshTokenResponseDTO)
# async def refresh_token(request: RefreshTokenRequest):
#     pass
