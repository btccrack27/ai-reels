from dataclasses import dataclass
from typing import List


@dataclass
class BRollContent:
    """
    B-Roll Content Entity.
    10 B-Roll Ideen, jeweils 3-5 Wörter.
    """
    ideas: List[str]  # Exakt 10 B-Roll Ideen

    def validate(self) -> None:
        """Validiert die B-Roll-Struktur"""
        if len(self.ideas) != 10:
            raise ValueError(
                f"Muss exakt 10 B-Roll Ideen enthalten, aber hat {len(self.ideas)}"
            )

        for i, idea in enumerate(self.ideas, 1):
            word_count = len(idea.split())
            if word_count < 3 or word_count > 5:
                raise ValueError(
                    f"B-Roll Idee {i} muss 3-5 Wörter haben, aber hat {word_count}: '{idea}'"
                )
