from dataclasses import dataclass


@dataclass
class VoiceoverContent:
    """
    Voiceover Content Entity.
    10-20 Sekunden Voiceover-Text.
    """
    text: str
    estimated_duration: int  # Geschätzte Dauer in Sekunden

    def validate(self) -> None:
        """Validiert den Voiceover-Text"""
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Voiceover-Text darf nicht leer sein")

        if self.estimated_duration < 10 or self.estimated_duration > 20:
            raise ValueError(
                f"Geschätzte Dauer muss 10-20 Sekunden sein, aber ist {self.estimated_duration}"
            )
