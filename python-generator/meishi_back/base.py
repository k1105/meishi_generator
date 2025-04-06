from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.renderPDF import draw
from svglib.svglib import svg2rlg
import os


class BaseBackDesign:
    def __init__(self, width_mm=91, height_mm=55):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.width_pt = width_mm * mm
        self.height_pt = height_mm * mm

    def draw_logo(self, c: canvas.Canvas, logo_path: str):
        """共通のロゴ描画処理"""
        try:
            drawing = svg2rlg(logo_path)

            # 最大サイズでフィットするようスケーリング
            available_width = self.width_pt - 20 * mm
            available_height = self.height_pt - 20 * mm
            scale_x = available_width / drawing.width
            scale_y = available_height / drawing.height
            scale = min(scale_x, scale_y)

            drawing.scale(scale, scale)

            pos_x = (self.width_pt - drawing.width * scale) / 2
            pos_y = (self.height_pt - drawing.height * scale) / 2

            draw(drawing, c, pos_x, pos_y)
        except Exception as e:
            print(f"⚠️ SVGロゴの描画中にエラーが発生しました: {e}")

    def generate(self, output_path: str, data: dict):
        """サブクラスで実装する必要があるメソッド"""
        try:
            # 出力ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # PDFの設定
            c = canvas.Canvas(
                output_path,
                pagesize=(self.width_pt, self.height_pt),
                pageCompression=1,  # 圧縮を有効化
                invariant=True  # 再現性を確保
            )

            # デザインの生成
            self._generate_design(c, data)

            # PDFを保存
            c.save()
            print(f"✅ 名刺の裏面を生成しました: {output_path}")

        except Exception as e:
            print(f"⚠️ 名刺の裏面の生成に失敗しました: {e}")
            import traceback
            print("詳細なエラー情報:")
            print(traceback.format_exc())

    def _generate_design(self, c: canvas.Canvas, data: dict):
        """サブクラスで実装する必要があるメソッド"""
        raise NotImplementedError("Subclasses must implement _generate_design()")
