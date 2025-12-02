from dataclasses import dataclass
from typing import List


@dataclass
class CaptionContent:
    """
    Caption Content Entity.
    Kurze Caption + exakt 15 Hashtags.
    """
    caption: str
    hashtags: List[str]  # Exakt 15 Hashtags

    def validate(self) -> None:
        """Validiert die Caption-Struktur"""
        if not self.caption or len(self.caption.strip()) == 0:
            raise ValueError("Caption darf nicht leer sein")

        if len(self.hashtags) != 15:
            raise ValueError(
                f"Muss exakt 15 Hashtags enthalten, aber hat {len(self.hashtags)}"
            )

        for i, hashtag in enumerate(self.hashtags, 1):
            if not hashtag.startswith('#'):
                raise ValueError(f"Hashtag {i} muss mit # beginnen: '{hashtag}'")

            if len(hashtag) <= 1:  # Nur "#" ohne Text
                raise ValueError(f"Hashtag {i} darf nicht leer sein")
