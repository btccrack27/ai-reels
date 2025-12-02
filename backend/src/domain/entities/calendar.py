from dataclasses import dataclass
from typing import Dict


@dataclass
class DayContent:
    """Content für einen einzelnen Tag im Content-Kalender"""
    day: int
    hook: str
    theme: str


@dataclass
class CalendarContent:
    """
    Calendar Content Entity.
    30-Tage Content-Plan mit Hook + Thema pro Tag.
    """
    niche: str  # Nische für die der Kalender erstellt wurde
    days: Dict[int, DayContent]  # 30 Tage (1-30)

    def validate(self) -> None:
        """Validiert die Calendar-Struktur"""
        if len(self.days) != 30:
            raise ValueError(
                f"Kalender muss exakt 30 Tage enthalten, aber hat {len(self.days)}"
            )

        for day_num in range(1, 31):
            if day_num not in self.days:
                raise ValueError(f"Tag {day_num} fehlt im Kalender")

            day = self.days[day_num]
            if day.day != day_num:
                raise ValueError(
                    f"Tag-Nummer stimmt nicht überein: erwartet {day_num}, aber ist {day.day}"
                )

            if not day.hook or len(day.hook.strip()) == 0:
                raise ValueError(f"Hook für Tag {day_num} darf nicht leer sein")

            if not day.theme or len(day.theme.strip()) == 0:
                raise ValueError(f"Thema für Tag {day_num} darf nicht leer sein")
