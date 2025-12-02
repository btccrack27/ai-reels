from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...application.dto.content_dto import (
    GenerateHookRequestDTO,
    GenerateScriptRequestDTO,
    GenerateShotlistRequestDTO,
    GenerateVoiceoverRequestDTO,
    GenerateCaptionRequestDTO,
    GenerateBRollRequestDTO,
    GenerateCalendarRequestDTO,
    HookResponseDTO,
    ScriptResponseDTO,
    ShotlistResponseDTO,
    VoiceoverResponseDTO,
    CaptionResponseDTO,
    BRollResponseDTO,
    CalendarResponseDTO,
    ContentListItemDTO,
    ContentDetailDTO
)
from ...application.use_cases.generate_hook_use_case import GenerateHookUseCase
from ...application.use_cases.generate_script_use_case import GenerateScriptUseCase
from ...application.use_cases.generate_shotlist_use_case import GenerateShotlistUseCase
from ...application.use_cases.generate_voiceover_use_case import GenerateVoiceoverUseCase
from ...application.use_cases.generate_caption_use_case import GenerateCaptionUseCase
from ...application.use_cases.generate_broll_use_case import GenerateBRollUseCase
from ...application.use_cases.generate_calendar_use_case import GenerateCalendarUseCase
from ..middlewares import get_current_user
from ..dependencies import (
    get_generate_hook_use_case,
    get_generate_script_use_case,
    get_generate_shotlist_use_case,
    get_generate_voiceover_use_case,
    get_generate_caption_use_case,
    get_generate_broll_use_case,
    get_generate_calendar_use_case
)
from pydantic import BaseModel


router = APIRouter(prefix="/api/content", tags=["content"])


# ============== Request Models ==============

class HookRequest(BaseModel):
    prompt: str
    context: str | None = None


class ScriptRequest(BaseModel):
    prompt: str
    context: str | None = None
    duration_seconds: int = 15


class ShotlistRequest(BaseModel):
    prompt: str
    context: str | None = None
    script: str | None = None


class VoiceoverRequest(BaseModel):
    prompt: str
    context: str | None = None
    script: str | None = None


class CaptionRequest(BaseModel):
    prompt: str
    context: str | None = None
    include_emojis: bool = True


class BRollRequest(BaseModel):
    prompt: str
    context: str | None = None


class CalendarRequest(BaseModel):
    niche: str
    prompt: str
    context: str | None = None


# ============== Endpoints ==============

@router.post("/hook", response_model=HookResponseDTO)
async def generate_hook(
    request: HookRequest,
    current_user: dict = Depends(get_current_user),
    use_case: GenerateHookUseCase = Depends(get_generate_hook_use_case)
):
    """
    Generiert 10 virale Hooks (5-10 Wörter).

    Requires: Authentication
    Rate-Limited: Ja (basierend auf Subscription Plan)
    """
    try:
        dto = GenerateHookRequestDTO(
            user_id=current_user["user_id"],
            prompt=request.prompt,
            context=request.context
        )
        result = await use_case.execute(dto)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei Hook-Generierung: {str(e)}"
        )


@router.post("/script", response_model=ScriptResponseDTO)
async def generate_script(
    request: ScriptRequest,
    current_user: dict = Depends(get_current_user),
    use_case: GenerateScriptUseCase = Depends(get_generate_script_use_case)
):
    """
    Generiert Reel-Script mit 2-4 Szenen (10-20 Sekunden).

    Requires: Authentication
    Rate-Limited: Ja
    """
    try:
        dto = GenerateScriptRequestDTO(
            user_id=current_user["user_id"],
            prompt=request.prompt,
            context=request.context,
            duration_seconds=request.duration_seconds
        )
        result = await use_case.execute(dto)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei Script-Generierung: {str(e)}"
        )


@router.post("/shotlist", response_model=ShotlistResponseDTO)
async def generate_shotlist(
    request: ShotlistRequest,
    current_user: dict = Depends(get_current_user),
    use_case: GenerateShotlistUseCase = Depends(get_generate_shotlist_use_case)
):
    """
    Generiert Shotlist mit 3-4 Shot Beschreibungen.

    Requires: Authentication
    Rate-Limited: Ja
    """
    try:
        dto = GenerateShotlistRequestDTO(
            user_id=current_user["user_id"],
            prompt=request.prompt,
            context=request.context,
            script=request.script
        )
        result = await use_case.execute(dto)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei Shotlist-Generierung: {str(e)}"
        )


@router.post("/voiceover", response_model=VoiceoverResponseDTO)
async def generate_voiceover(
    request: VoiceoverRequest,
    current_user: dict = Depends(get_current_user),
    use_case: GenerateVoiceoverUseCase = Depends(get_generate_voiceover_use_case)
):
    """
    Generiert Voiceover Text (10-20 Sekunden).

    Requires: Authentication
    Rate-Limited: Ja
    """
    try:
        dto = GenerateVoiceoverRequestDTO(
            user_id=current_user["user_id"],
            prompt=request.prompt,
            context=request.context,
            script=request.script
        )
        result = await use_case.execute(dto)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei Voiceover-Generierung: {str(e)}"
        )


@router.post("/caption", response_model=CaptionResponseDTO)
async def generate_caption(
    request: CaptionRequest,
    current_user: dict = Depends(get_current_user),
    use_case: GenerateCaptionUseCase = Depends(get_generate_caption_use_case)
):
    """
    Generiert Instagram Caption mit 15 Hashtags.

    Requires: Authentication
    Rate-Limited: Ja
    """
    try:
        dto = GenerateCaptionRequestDTO(
            user_id=current_user["user_id"],
            prompt=request.prompt,
            context=request.context,
            include_emojis=request.include_emojis
        )
        result = await use_case.execute(dto)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei Caption-Generierung: {str(e)}"
        )


@router.post("/broll", response_model=BRollResponseDTO)
async def generate_broll(
    request: BRollRequest,
    current_user: dict = Depends(get_current_user),
    use_case: GenerateBRollUseCase = Depends(get_generate_broll_use_case)
):
    """
    Generiert 10 B-Roll Ideen (3-5 Wörter).

    Requires: Authentication
    Rate-Limited: Ja
    """
    try:
        dto = GenerateBRollRequestDTO(
            user_id=current_user["user_id"],
            prompt=request.prompt,
            context=request.context
        )
        result = await use_case.execute(dto)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei B-Roll-Generierung: {str(e)}"
        )


@router.post("/calendar", response_model=CalendarResponseDTO)
async def generate_calendar(
    request: CalendarRequest,
    current_user: dict = Depends(get_current_user),
    use_case: GenerateCalendarUseCase = Depends(get_generate_calendar_use_case)
):
    """
    Generiert 30-Tage Content-Kalender.

    Requires: Authentication
    Rate-Limited: Ja
    """
    try:
        dto = GenerateCalendarRequestDTO(
            user_id=current_user["user_id"],
            niche=request.niche,
            prompt=request.prompt,
            context=request.context
        )
        result = await use_case.execute(dto)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler bei Kalender-Generierung: {str(e)}"
        )


# TODO: Implement content history and detail endpoints
# @router.get("/history", response_model=List[ContentListItemDTO])
# @router.get("/{content_id}", response_model=ContentDetailDTO)
