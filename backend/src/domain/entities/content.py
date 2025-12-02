from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


class ContentType(str, Enum):
    """Typ des generierten Contents"""
    HOOK = "hook"
    SCRIPT = "script"
    SHOTLIST = "shotlist"
    VOICEOVER = "voiceover"
    CAPTION = "caption"
    BROLL = "broll"
    CALENDAR = "calendar"


class ContentStatus(str, Enum):
    """Status der Content-Generierung"""
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Content:
    """
    Basis-Entity für alle generierten Contents.
    Polymorphisches Design: data-Feld enthält typ-spezifische Daten.
    """
    id: str
    user_id: str
    type: ContentType
    status: ContentStatus
    data: Any  # Polymorphisch - Struktur abhängig vom ContentType
    prompt: str  # Original User-Prompt
    version: int  # Content-Versionierung
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None  # Zusätzlicher Kontext
