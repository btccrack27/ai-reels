from dataclasses import dataclass
from typing import List


@dataclass
class HookContent:
    """
    Hook Content Entity.
    Enthält genau 10 virale Hooks, jeweils 5-10 Wörter lang.
    """
    hooks: List[str]  # Exakt 10 Hooks

    def validate(self) -> None:
        """Validiert die Hook-Struktur"""
        if len(self.hooks) != 10:
            raise ValueError(f"Muss exakt 10 Hooks enthalten, aber hat {len(self.hooks)}")

        for i, hook in enumerate(self.hooks, 1):
            word_count = len(hook.split())
            if word_count < 5 or word_count > 10:
                raise ValueError(
                    f"Hook {i} muss 5-10 Wörter haben, aber hat {word_count}: '{hook}'"
                )
