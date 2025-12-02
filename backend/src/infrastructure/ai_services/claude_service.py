import os
import json
from typing import List, Dict, Tuple
from anthropic import AsyncAnthropic
from ...domain.entities.hook import HookContent
from ...domain.entities.script import ScriptContent, SceneContent
from ...domain.entities.shotlist import ShotlistContent
from ...domain.entities.voiceover import VoiceoverContent
from ...domain.entities.caption import CaptionContent
from ...domain.entities.broll import BRollContent
from ...domain.entities.calendar import CalendarContent, DayContent
from .claude_prompts import (
    HOOK_SYSTEM_PROMPT,
    SCRIPT_SYSTEM_PROMPT,
    SHOTLIST_SYSTEM_PROMPT,
    VOICEOVER_SYSTEM_PROMPT,
    CAPTION_SYSTEM_PROMPT,
    BROLL_SYSTEM_PROMPT,
    CALENDAR_SYSTEM_PROMPT
)


class ClaudeService:
    """
    Claude API Service für Content-Generierung.
    Verwendet Claude 3.5 Sonnet für alle 7 Content-Typen.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY nicht gesetzt")

        self.client = AsyncAnthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 2048

    async def generate_hooks(self, prompt: str, context: str = None) -> HookContent:
        """
        Generiert 10 virale Hooks (5-10 Wörter).

        Args:
            prompt: User-Thema/Prompt
            context: Optional zusätzlicher Kontext

        Returns:
            HookContent mit 10 Hooks
        """
        user_message = f"Thema: {prompt}"
        if context:
            user_message += f"\n\nKontext: {context}"

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.8,
            system=HOOK_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        # Parse JSON Response
        content = response.content[0].text
        data = json.loads(content)

        return HookContent(hooks=data["hooks"])

    async def generate_script(
        self,
        prompt: str,
        target_audience: str = None,
        tone: str = "engaging"
    ) -> ScriptContent:
        """
        Generiert Reel-Script mit 2-4 Szenen (10-20 Sekunden).

        Args:
            prompt: User-Thema/Prompt
            target_audience: Zielgruppe
            tone: Tonalität (engaging, professional, casual)

        Returns:
            ScriptContent mit Szenen und CTA
        """
        user_message = f"Thema: {prompt}\nTon: {tone}"
        if target_audience:
            user_message += f"\nZielgruppe: {target_audience}"

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.8,
            system=SCRIPT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        content = response.content[0].text
        data = json.loads(content)

        # Build SceneContent objects
        scenes = [
            SceneContent(
                scene_number=scene["scene_number"],
                type=scene["type"],
                text=scene["text"],
                duration_seconds=scene["duration_seconds"],
                visual_description=scene["visual_description"]
            )
            for scene in data["scenes"]
        ]

        return ScriptContent(
            scenes=scenes,
            cta=data["cta"],
            total_duration=data["total_duration"]
        )

    async def generate_shotlist(self, script: str) -> ShotlistContent:
        """
        Generiert 3-4 Shot-Beschreibungen für ein Script.

        Args:
            script: Das Reel-Script

        Returns:
            ShotlistContent mit 3-4 Shots
        """
        user_message = f"Script:\n{script}"

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.7,
            system=SHOTLIST_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        content = response.content[0].text
        data = json.loads(content)

        return ShotlistContent(shots=data["shots"])

    async def generate_voiceover(self, script: str) -> VoiceoverContent:
        """
        Generiert Voiceover-Text (10-20 Sekunden).

        Args:
            script: Das Reel-Script

        Returns:
            VoiceoverContent mit Text
        """
        user_message = f"Script:\n{script}"

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.7,
            system=VOICEOVER_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        content = response.content[0].text
        data = json.loads(content)

        return VoiceoverContent(
            text=data["text"],
            estimated_duration=data["estimated_duration"]
        )

    async def generate_caption(self, theme: str) -> CaptionContent:
        """
        Generiert Caption + 15 Hashtags.

        Args:
            theme: Thema/Content des Reels

        Returns:
            CaptionContent mit Caption und Hashtags
        """
        user_message = f"Thema: {theme}"

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.8,
            system=CAPTION_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        content = response.content[0].text
        data = json.loads(content)

        return CaptionContent(
            caption=data["caption"],
            hashtags=data["hashtags"]
        )

    async def generate_broll_ideas(self, theme: str) -> BRollContent:
        """
        Generiert 10 B-Roll Ideen (3-5 Wörter).

        Args:
            theme: Thema des Reels

        Returns:
            BRollContent mit 10 Ideen
        """
        user_message = f"Thema: {theme}"

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.8,
            system=BROLL_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        content = response.content[0].text
        data = json.loads(content)

        return BRollContent(ideas=data["ideas"])

    async def generate_calendar(
        self,
        niche: str,
        target_audience: str,
        goals: List[str] = None
    ) -> CalendarContent:
        """
        Generiert 30-Tage Content-Kalender.

        Args:
            niche: Nische/Themenbereich
            target_audience: Zielgruppe
            goals: Optional Liste von Zielen

        Returns:
            CalendarContent mit 30 Tagen
        """
        user_message = f"Nische: {niche}\nZielgruppe: {target_audience}"
        if goals:
            user_message += f"\nZiele: {', '.join(goals)}"

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,  # Mehr Tokens für 30 Tage
            temperature=0.8,
            system=CALENDAR_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        content = response.content[0].text
        data = json.loads(content)

        # Build DayContent objects
        days = {}
        for day_num, day_data in data["days"].items():
            days[int(day_num)] = DayContent(
                day=int(day_num),
                hook=day_data["hook"],
                theme=day_data["theme"]
            )

        return CalendarContent(
            niche=niche,
            days=days
        )
