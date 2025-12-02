from dataclasses import dataclass
from typing import List


@dataclass
class ShotlistContent:
    """
    Shotlist Content Entity.
    Idiotensichere Shotlist mit 3-4 Shots.
    """
    shots: List[str]  # 3-4 Shot-Beschreibungen

    def validate(self) -> None:
        """Validiert die Shotlist-Struktur"""
        if len(self.shots) < 3 or len(self.shots) > 4:
            raise ValueError(
                f"Shotlist muss 3-4 Shots enthalten, aber hat {len(self.shots)}"
            )

        for i, shot in enumerate(self.shots, 1):
            if not shot or len(shot.strip()) == 0:
                raise ValueError(f"Shot {i} darf nicht leer sein")
