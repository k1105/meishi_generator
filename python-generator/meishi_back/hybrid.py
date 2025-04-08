from .base import BaseBackDesign
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
import os
from .utils import draw_hybrid_grid
from reportlab.lib.colors import Color


class HybridBackDesign(BaseBackDesign):
    def _generate_design(self, c: canvas.Canvas, data: dict):
        """Hybridタイプの裏面デザインを生成"""
        # ロゴのパスを取得
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "DL_LOGO_HorizontalStacked_Black_CMYK.svg")
        
        # ロゴのサイズと位置を計算
        logo_width, logo_height = self.calculate_logo_size(data)
        logo_x, logo_y = self.calculate_logo_position(data, logo_width, logo_height)
        
        # 背景色を設定
        c.setFillColor(Color(1, 1, 1))  # 白
        c.rect(0, 0, self.width_mm * 2.8346, self.height_mm * 2.8346, fill=1)  # 1mm = 2.8346pt
        
        # 名刺のサイズを計算（px単位）
        meishi_width = 257.95
        meishi_height = 155.91
        
        # 3mmをpx単位に変換（1mm = 2.8346px）
        margin_px = 3 * 2.8346
        
        # グリッドの描画に使用するスケールを計算（フロントエンドと同じ計算方法）
        base_scale = 2
        minimum_grid_size = 4.96 * base_scale
        
        # detailednessの値を取得してminimum_grid_sizeに掛け合わせる
        detailedness = data.get("pattern", {}).get("grid", {}).get("detailedness", 1.0)
        grid_size = minimum_grid_size * detailedness
        
        # ハイブリッドグリッドを描画
        draw_hybrid_grid(c, margin_px, margin_px, meishi_width, meishi_height,
                        logo_x + margin_px, logo_y + margin_px, logo_width, logo_height,
                        grid_size)
        
        # ロゴを描画
        self.draw_logo(c, logo_path, logo_x + margin_px, logo_y + margin_px, logo_width, logo_height)
