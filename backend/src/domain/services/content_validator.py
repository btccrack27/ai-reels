from typing import Any
from ..entities.content import ContentType
from ..entities.hook import HookContent
from ..entities.script import ScriptContent
from ..entities.shotlist import ShotlistContent
from ..entities.voiceover import VoiceoverContent
from ..entities.caption import CaptionContent
from ..entities.broll import BRollContent
from ..entities.calendar import CalendarContent


class ContentValidator:
    """
    Domain Service für Content-Validierung.
    Validiert generierte Contents basierend auf ihrem Typ.
    """

    def validate(self, content_type: ContentType, data: Any) -> tuple[bool, str]:
        """
        Validiert Content-Daten.

        Args:
            content_type: Typ des Contents
            data: Die zu validierenden Daten

        Returns:
            (is_valid: bool, error_message: str)
        """
        try:
            if content_type == ContentType.HOOK:
                hook = HookContent(**data)
                hook.validate()

            elif content_type == ContentType.SCRIPT:
                script = ScriptContent(**data)
                script.validate()

            elif content_type == ContentType.SHOTLIST:
                shotlist = ShotlistContent(**data)
                shotlist.validate()

            elif content_type == ContentType.VOICEOVER:
                voiceover = VoiceoverContent(**data)
                voiceover.validate()

            elif content_type == ContentType.CAPTION:
                caption = CaptionContent(**data)
                caption.validate()

            elif content_type == ContentType.BROLL:
                broll = BRollContent(**data)
                broll.validate()

            elif content_type == ContentType.CALENDAR:
                calendar = CalendarContent(**data)
                calendar.validate()

            else:
                return False, f"Unbekannter Content-Typ: {content_type}"

            return True, ""

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Validierungs-Fehler: {str(e)}"

    def validate_prompt(self, prompt: str, min_length: int = 10, max_length: int = 500) -> tuple[bool, str]:
        """
        Validiert einen User-Prompt.

        Args:
            prompt: Der zu validierende Prompt
            min_length: Minimale Länge
            max_length: Maximale Länge

        Returns:
            (is_valid: bool, error_message: str)
        """
        if not prompt or len(prompt.strip()) == 0:
            return False, "Prompt darf nicht leer sein"

        prompt_length = len(prompt.strip())

        if prompt_length < min_length:
            return False, f"Prompt zu kurz (min. {min_length} Zeichen)"

        if prompt_length > max_length:
            return False, f"Prompt zu lang (max. {max_length} Zeichen)"

        return True, ""
