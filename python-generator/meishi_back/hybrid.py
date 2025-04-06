from .base import BaseBackDesign
from reportlab.pdfgen import canvas
import os


class HybridBackDesign(BaseBackDesign):
    def _generate_design(self, c: canvas.Canvas, data: dict):
        """Hybridタイプの裏面デザインを生成"""
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "DL_LOGO_HorizontalStacked_Black_CMYK.svg")
        self.draw_logo(c, logo_path)
