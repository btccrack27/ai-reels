from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from ...domain.entities.hook import HookContent
from ...domain.entities.script import ScriptContent
from ...domain.entities.shotlist import ShotlistContent
from ...domain.entities.voiceover import VoiceoverContent
from ...domain.entities.caption import CaptionContent
from ...domain.entities.broll import BRollContent
from ...domain.entities.calendar import CalendarContent


class PDFGenerator:
    """
    PDF Generator für alle Content-Typen.
    Verwendet ReportLab für professionelle PDFs.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Erstellt custom Styles für Branding"""
        # Title Style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0284c7'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtitle Style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0369a1'),
            spaceAfter=20,
            fontName='Helvetica-Bold'
        ))

        # Item Style
        self.styles.add(ParagraphStyle(
            name='CustomItem',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            leftIndent=20
        ))

    def _add_header(self, story, title: str):
        """Fügt Header mit Branding hinzu"""
        story.append(Paragraph("AI Reels Generator", self.styles['CustomTitle']))
        story.append(Paragraph(title, self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.5*cm))

    def _add_footer(self, story):
        """Fügt Footer hinzu"""
        story.append(Spacer(1, 1*cm))
        footer_text = f"Generiert am {datetime.now().strftime('%d.%m.%Y um %H:%M')} Uhr"
        footer_style = ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT
        )
        story.append(Paragraph(footer_text, footer_style))

    def generate_hook_pdf(self, content: HookContent, prompt: str) -> bytes:
        """Generiert PDF für Hooks"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Header
        self._add_header(story, "10 Virale Hooks")

        # Prompt
        story.append(Paragraph(f"<b>Thema:</b> {prompt}", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Hooks als nummerierte Liste
        for i, hook in enumerate(content.hooks, 1):
            hook_text = f"<b>{i}.</b> {hook}"
            story.append(Paragraph(hook_text, self.styles['CustomItem']))

        # Footer
        self._add_footer(story)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_script_pdf(self, content: ScriptContent, prompt: str) -> bytes:
        """Generiert PDF für Script"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Header
        self._add_header(story, "Reel Script")

        # Prompt
        story.append(Paragraph(f"<b>Thema:</b> {prompt}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Gesamtdauer:</b> {content.total_duration} Sekunden", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Szenen
        for scene in content.scenes:
            # Szenen-Header
            scene_header = f"<b>Szene {scene.scene_number}</b> ({scene.type}) - {scene.duration_seconds}s"
            story.append(Paragraph(scene_header, self.styles['Heading3']))

            # Text
            story.append(Paragraph(f"<b>Text:</b> {scene.text}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Visual:</b> {scene.visual_description}", self.styles['Normal']))
            story.append(Spacer(1, 0.3*cm))

        # CTA
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("<b>Call to Action:</b>", self.styles['Heading3']))
        story.append(Paragraph(content.cta, self.styles['Normal']))

        # Footer
        self._add_footer(story)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_shotlist_pdf(self, content: ShotlistContent, prompt: str) -> bytes:
        """Generiert PDF für Shotlist"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Header
        self._add_header(story, "Shot List")

        # Prompt
        story.append(Paragraph(f"<b>Thema:</b> {prompt}", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Shots als Tabelle
        data = [['#', 'Shot Beschreibung']]
        for i, shot in enumerate(content.shots, 1):
            data.append([str(i), shot])

        table = Table(data, colWidths=[1*cm, 15*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)

        # Footer
        self._add_footer(story)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_voiceover_pdf(self, content: VoiceoverContent, prompt: str) -> bytes:
        """Generiert PDF für Voiceover"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Header
        self._add_header(story, "Voiceover Script")

        # Prompt & Duration
        story.append(Paragraph(f"<b>Thema:</b> {prompt}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Dauer:</b> ca. {content.estimated_duration} Sekunden", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Voiceover Text in Box
        vo_style = ParagraphStyle(
            name='VoiceoverBox',
            parent=self.styles['Normal'],
            fontSize=12,
            leading=18,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10
        )
        story.append(Paragraph(content.text, vo_style))

        # Footer
        self._add_footer(story)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_caption_pdf(self, content: CaptionContent, prompt: str) -> bytes:
        """Generiert PDF für Caption"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Header
        self._add_header(story, "Instagram Caption")

        # Prompt
        story.append(Paragraph(f"<b>Thema:</b> {prompt}", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Caption
        story.append(Paragraph("<b>Caption:</b>", self.styles['Heading3']))
        story.append(Paragraph(content.caption, self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Hashtags
        story.append(Paragraph("<b>Hashtags:</b>", self.styles['Heading3']))
        hashtags_text = " ".join(content.hashtags)
        story.append(Paragraph(hashtags_text, self.styles['Normal']))

        # Footer
        self._add_footer(story)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_broll_pdf(self, content: BRollContent, prompt: str) -> bytes:
        """Generiert PDF für B-Roll Ideas"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Header
        self._add_header(story, "B-Roll Ideen")

        # Prompt
        story.append(Paragraph(f"<b>Thema:</b> {prompt}", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # B-Roll Ideas als Liste
        for i, idea in enumerate(content.ideas, 1):
            idea_text = f"<b>{i}.</b> {idea}"
            story.append(Paragraph(idea_text, self.styles['CustomItem']))

        # Footer
        self._add_footer(story)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_calendar_pdf(self, content: CalendarContent, prompt: str) -> bytes:
        """Generiert PDF für 30-Tage Kalender"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Header
        self._add_header(story, "30-Tage Content Kalender")

        # Nische
        story.append(Paragraph(f"<b>Nische:</b> {content.niche}", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Kalender als Tabelle (split in 2 Seiten: Tag 1-15 und 16-30)
        # Seite 1: Tag 1-15
        data1 = [['Tag', 'Hook', 'Thema']]
        for day_num in range(1, 16):
            day = content.days[day_num]
            data1.append([str(day_num), day.hook, day.theme])

        table1 = Table(data1, colWidths=[1.5*cm, 7*cm, 7*cm])
        table1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(table1)

        # Page Break
        story.append(PageBreak())

        # Seite 2: Tag 16-30
        data2 = [['Tag', 'Hook', 'Thema']]
        for day_num in range(16, 31):
            day = content.days[day_num]
            data2.append([str(day_num), day.hook, day.theme])

        table2 = Table(data2, colWidths=[1.5*cm, 7*cm, 7*cm])
        table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(table2)

        # Footer
        self._add_footer(story)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
