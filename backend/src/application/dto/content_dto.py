from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime
from ...domain.entities.content import ContentType, ContentStatus


# ================== Request DTOs ==================

@dataclass
class GenerateContentRequestDTO:
    """Base DTO für Content-Generierung Requests"""
    user_id: str
    prompt: str
    context: Optional[str] = None


@dataclass
class GenerateHookRequestDTO(GenerateContentRequestDTO):
    """Request für Hook-Generierung"""
    pass


@dataclass
class GenerateScriptRequestDTO(GenerateContentRequestDTO):
    """Request für Script-Generierung"""
    duration_seconds: int = 15  # Default: 15 Sekunden


@dataclass
class GenerateShotlistRequestDTO(GenerateContentRequestDTO):
    """Request für Shotlist-Generierung"""
    script: Optional[str] = None  # Optional: basierend auf existierendem Script


@dataclass
class GenerateVoiceoverRequestDTO(GenerateContentRequestDTO):
    """Request für Voiceover-Generierung"""
    script: Optional[str] = None  # Optional: basierend auf existierendem Script


@dataclass
class GenerateCaptionRequestDTO(GenerateContentRequestDTO):
    """Request für Caption-Generierung"""
    include_emojis: bool = True


@dataclass
class GenerateBRollRequestDTO(GenerateContentRequestDTO):
    """Request für B-Roll Ideas-Generierung"""
    pass


@dataclass
class GenerateCalendarRequestDTO(GenerateContentRequestDTO):
    """Request für 30-Tage Kalender-Generierung"""
    niche: Optional[str] = None  # Die Nische/Thema für den Content-Plan (wird aus prompt verwendet wenn nicht angegeben)


# ================== Response DTOs ==================

@dataclass
class HookResponseDTO:
    """Response für generierte Hooks"""
    id: str
    hooks: List[str]
    prompt: str
    created_at: datetime


@dataclass
class SceneDTO:
    """DTO für eine Script-Szene"""
    scene_number: int
    type: str  # hook, content, cta
    text: str
    visual_description: str
    duration_seconds: int


@dataclass
class ScriptResponseDTO:
    """Response für generiertes Script"""
    id: str
    scenes: List[SceneDTO]
    cta: str
    total_duration: int
    prompt: str
    created_at: datetime


@dataclass
class ShotlistResponseDTO:
    """Response für generierte Shotlist"""
    id: str
    shots: List[str]
    prompt: str
    created_at: datetime


@dataclass
class VoiceoverResponseDTO:
    """Response für generierten Voiceover"""
    id: str
    text: str
    estimated_duration: int
    prompt: str
    created_at: datetime


@dataclass
class CaptionResponseDTO:
    """Response für generierte Caption"""
    id: str
    caption: str
    hashtags: List[str]
    prompt: str
    created_at: datetime


@dataclass
class BRollResponseDTO:
    """Response für generierte B-Roll Ideas"""
    id: str
    ideas: List[str]
    prompt: str
    created_at: datetime


@dataclass
class DayContentDTO:
    """DTO für einen Tag im Content-Kalender"""
    day: int
    hook: str
    theme: str


@dataclass
class CalendarResponseDTO:
    """Response für generierten 30-Tage Kalender"""
    id: str
    niche: str
    days: List[DayContentDTO]
    prompt: str
    created_at: datetime


# ================== Generic Content DTOs ==================

@dataclass
class ContentListItemDTO:
    """DTO für Content-Liste (History)"""
    id: str
    type: ContentType
    status: ContentStatus
    prompt: str
    created_at: datetime
    preview: str  # Kurze Vorschau des Contents


@dataclass
class ContentDetailDTO:
    """DTO für Content-Details (beliebiger Typ)"""
    id: str
    user_id: str
    type: ContentType
    status: ContentStatus
    data: Any  # Polymorphisch - typ-spezifische Daten
    prompt: str
    version: int
    created_at: datetime
    updated_at: datetime


# ================== PDF Export DTOs ==================

@dataclass
class ExportPDFRequestDTO:
    """Request für PDF Export"""
    user_id: str
    content_id: str


@dataclass
class ExportPDFResponseDTO:
    """Response für PDF Export"""
    content_id: str
    content_type: ContentType
    pdf_bytes: bytes
    filename: str
