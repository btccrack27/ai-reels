from dataclasses import dataclass
from typing import List


@dataclass
class SceneContent:
    """Einzelne Szene im Reel-Script"""
    scene_number: int
    type: str  # "Facecam", "B-Roll", "Overlay"
    text: str
    duration_seconds: float
    visual_description: str


@dataclass
class ScriptContent:
    """
    Script Content Entity.
    Reel-Script mit 2-4 Szenen, insgesamt 10-20 Sekunden.
    """
    scenes: List[SceneContent]  # 2-4 Szenen
    cta: str  # Call to Action
    total_duration: int  # Gesamtdauer in Sekunden

    def validate(self) -> None:
        """Validiert die Script-Struktur"""
        if len(self.scenes) < 2 or len(self.scenes) > 4:
            raise ValueError(
                f"Script muss 2-4 Szenen haben, aber hat {len(self.scenes)}"
            )

        if self.total_duration < 10 or self.total_duration > 20:
            raise ValueError(
                f"Gesamtdauer muss 10-20 Sekunden sein, aber ist {self.total_duration}"
            )

        if not self.cta or len(self.cta.strip()) == 0:
            raise ValueError("CTA darf nicht leer sein")
