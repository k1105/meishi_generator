from .base import BaseBackDesign
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
import os
from .utils import draw_hybrid_grid


class HybridBackDesign(BaseBackDesign):
    def _generate_design(self, c: canvas.Canvas, data: dict):
        """Hybridタイプの裏面デザインを生成"""
        # ロゴのパスを取得
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "DL_LOGO_HorizontalStacked_Black_CMYK.svg")
        
        # ロゴのサイズと位置を計算
        logo_width = self.width_pt * 0.6  # ロゴの幅を名刺の60%に設定
        logo_height = self.height_pt * 0.3  # ロゴの高さを名刺の30%に設定
        logo_x = (self.width_pt - logo_width) / 2  # 中央揃え
        logo_y = (self.height_pt - logo_height) / 2  # 中央揃え
        
        # 背景色を設定
        c.setFillColorRGB(1, 1, 1)  # 白
        c.rect(0, 0, self.width_pt, self.height_pt, fill=1)
        
        # ハイブリッドグリッドを描画
        unit_size = 5 * mm  # グリッドの単位サイズ
        draw_hybrid_grid(c, 0, 0, self.width_pt, self.height_pt,
                        logo_x, logo_y, logo_width, logo_height,
                        unit_size)
        
        # ロゴを描画
        self.draw_logo(c, logo_path)
