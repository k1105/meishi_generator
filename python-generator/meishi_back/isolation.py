from .base import BaseBackDesign
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
import os
from .utils import draw_isolation_grid
import xml.etree.ElementTree as ET


class IsolationBackDesign(BaseBackDesign):
    def _generate_design(self, c: canvas.Canvas, data: dict):
        """Isolationタイプの裏面デザインを生成"""
        # ロゴのパスを取得
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "DL_LOGO_HorizontalStacked_Black_CMYK.svg")
        
        # SVGファイルから元のロゴ画像の高さを取得
        tree = ET.parse(logo_path)
        root = tree.getroot()
        view_box = root.get('viewBox')
        if view_box:
            _, _, _, original_height = map(float, view_box.split())
            original_logo_height = original_height
        else:
            original_logo_height = 100  # デフォルト値
        
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
        max_grid_size = minimum_grid_size * 4
        
        # サイズリスト（ロゴサイズの定義）
        size_list = {
            'l': max_grid_size * 5,
            'm': max_grid_size * 4,
            's': max_grid_size * 3,
            'xs': max_grid_size * 2
        }
        
        # patternオブジェクトからsizeを取得
        target_size = size_list.get(data.get("pattern", {}).get("size", "m"), size_list["m"])
        
        # imageScaleを計算
        image_scale = (target_size / original_logo_height)*5
        
        # アイソレーショングリッドを描画
        draw_isolation_grid(c, margin_px, margin_px, meishi_width, meishi_height,
                           logo_x + margin_px, logo_y + margin_px, logo_width, logo_height,
                           image_scale)
        
        # ロゴを描画
        self.draw_logo(c, logo_path, logo_x + margin_px, logo_y + margin_px, logo_width, logo_height)
