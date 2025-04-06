from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


class FrontDesign:
    def __init__(self, width_mm=91, height_mm=55):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.width_pt = width_mm * mm
        self.height_pt = height_mm * mm

        # SVGのviewBoxサイズ
        self.svg_width = 275.05
        self.svg_height = 172.96

        # スケールファクター
        self.scale_x = self.width_pt / self.svg_width
        self.scale_y = self.height_pt / self.svg_height

        # フォントの設定
        self.setup_fonts()

    def svg_to_pdf(self, x, y):
        """SVG座標をPDF座標に変換"""
        pdf_x = x * self.scale_x
        pdf_y = self.height_pt - (y * self.scale_y)  # Y座標を反転
        return pdf_x, pdf_y

    def setup_fonts(self):
        """フォントの設定"""
        try:
            # フォントディレクトリのパスを取得
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            font_dir = os.path.join(base_dir, "fonts")
            print(f"📁 フォントディレクトリ: {font_dir}")

            # 日本語フォント
            jp_font_path = os.path.join(font_dir, "NotoSansJP-Bold.ttf")
            pdfmetrics.registerFont(TTFont('NotoSansJP-Bold', jp_font_path))
            print(f"✅ 日本語フォントを登録: {jp_font_path}")

            # 英語フォント
            en_font_path = os.path.join(font_dir, "Inter_18pt-Bold.ttf")
            pdfmetrics.registerFont(TTFont('Inter-Bold', en_font_path))
            print(f"✅ 英語フォントを登録: {en_font_path}")

            # モノスペースフォント
            mono_font_path = os.path.join(font_dir, "IBMPlexMono-Regular.ttf")
            pdfmetrics.registerFont(TTFont('IBMPlexMono', mono_font_path))
            print(f"✅ モノスペースフォントを登録: {mono_font_path}")

            # フォントの代替設定
            self.font_mapping = {
                'NotoSansJP-Bold': 'NotoSansJP-Bold',
                'Inter-Bold': 'Inter-Bold',
                'IBMPlexMono': 'IBMPlexMono'
            }

        except Exception as e:
            print(f"⚠️ フォントの設定に失敗しました: {e}")
            import traceback
            print("詳細なエラー情報:")
            print(traceback.format_exc())
            # フォントが見つからない場合は、デフォルトフォントを使用
            self.font_mapping = {
                'NotoSansJP-Bold': 'Helvetica',
                'Inter-Bold': 'Helvetica-Bold',
                'IBMPlexMono': 'Courier'
            }
            print("⚠️ デフォルトフォントを使用します")

    def draw_guide_lines(self, c: canvas.Canvas):
        """ガイドラインの描画"""
        c.setStrokeColorRGB(0.45, 0.45, 0.45)  # #727171
        c.setLineWidth(0.2)

        # 水平線
        x1, y1 = self.svg_to_pdf(0, 99.57)
        x2, y2 = self.svg_to_pdf(self.svg_width, 99.57)
        c.line(x1, y1, x2, y2)

        # 垂直線
        x1, y1 = self.svg_to_pdf(168.84, 99.57)
        x2, y2 = self.svg_to_pdf(168.84, self.svg_height)
        c.line(x1, y1, x2, y2)

        # 斜めの線
        x1, y1 = self.svg_to_pdf(214.3, 99.57)
        x2, y2 = self.svg_to_pdf(214.3, 0.05)
        c.line(x1, y1, x2, y2)

        x1, y1 = self.svg_to_pdf(214.3, 99.57)
        x2, y2 = self.svg_to_pdf(271.33, 0.05)
        c.line(x1, y1, x2, y2)

        x1, y1 = self.svg_to_pdf(209.55, 0.05)
        x2, y2 = self.svg_to_pdf(274.96, 114.44)
        c.line(x1, y1, x2, y2)

    def draw_text(self, c: canvas.Canvas, text: str, x: float, y: float, font_name: str, font_size: float, color: tuple = (0, 0, 0)):
        """テキストを描画"""
        c.saveState()
        try:
            # フォントの設定
            c.setFont(font_name, font_size)
            c.setFillColorRGB(*color)

            # テキストの描画
            if font_name == "IBMPlexMono":
                # モノスペースフォントの場合は文字間隔を調整
                char_width = c.stringWidth(" ", font_name, font_size)
                for i, char in enumerate(text):
                    c.drawString(x + i * char_width, y, char)
            else:
                c.drawString(x, y, text)
        finally:
            c.restoreState()

    def generate(self, c: canvas.Canvas, data: dict):
        """表面のデザインを生成"""
        self.draw_guide_lines(c)
        self.draw_text(c, data.get("nameJa", "（漢字名未定義）"), *self.svg_to_pdf(32.55, 55.7), self.font_mapping['NotoSansJP-Bold'], 9.5)
        self.draw_text(c, data.get("name", "KANATA YAMAGISHI"), *self.svg_to_pdf(81.48, 54.6), self.font_mapping['Inter-Bold'], 7.0)
        self.draw_text(c, "HEAD OF DESIGN / DENTSU LAB TOKYO", *self.svg_to_pdf(32.06, 68.16), self.font_mapping['IBMPlexMono'], 6.0)
        self.draw_text(c, "E-MAIL:", *self.svg_to_pdf(32.05, 116.93), self.font_mapping['IBMPlexMono'], 4.5)
        self.draw_text(c, data.get("email", "example@example.com"), *self.svg_to_pdf(32.42, 125.85), self.font_mapping['Inter-Bold'], 6.5)
        self.draw_text(c, "PHONE:", *self.svg_to_pdf(32.05, 138.48), self.font_mapping['IBMPlexMono'], 4.5)
        self.draw_text(c, "+81 80-6803-5201", *self.svg_to_pdf(32.27, 147.41), self.font_mapping['Inter-Bold'], 6.5) 