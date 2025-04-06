from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
import os
import reportlab.graphics.renderPDF as renderPDF


class QRPlacement:
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

    def svg_to_pdf(self, x, y):
        """SVG座標をPDF座標に変換"""
        pdf_x = x * self.scale_x
        pdf_y = self.height_pt - (y * self.scale_y)  # Y座標を反転
        return pdf_x, pdf_y

    def place(self, c: canvas.Canvas):
        """QRコードを配置"""
        try:
            # QRコードの位置を計算（SVGの座標からPDFの座標に変換）
            x, y = self.svg_to_pdf(205.4672, 144.6592)
            qr_width = 28.35 * self.scale_x
            qr_height = 28.35 * self.scale_y

            print(f"📍 QRコードの配置位置: x={x:.2f}, y={y:.2f}")
            print(f"📏 QRコードのサイズ: {qr_width:.2f}x{qr_height:.2f}pt")
            print(f"📏 名刺のサイズ: {self.width_pt}x{self.height_pt}pt")

            # QRコードのSVGファイルのパスを取得
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            qr_svg_path = os.path.join(base_dir, "assets", "qr.svg")

            if not os.path.exists(qr_svg_path):
                print(f"⚠️ QRコードのSVGファイルが見つかりません: {qr_svg_path}")
                return

            print(f"📁 QRコードのSVGファイルを読み込み: {qr_svg_path}")

            # SVGを描画オブジェクトに変換
            drawing = svg2rlg(qr_svg_path)
            if drawing is None:
                print("⚠️ SVGの変換に失敗しました")
                return

            print(f"📐 SVGのサイズ: {drawing.width}x{drawing.height}")

            # 描画オブジェクトを指定位置に描画
            c.saveState()
            try:
                # 背景を白色で塗りつぶし
                c.setFillColorRGB(1, 1, 1)
                c.rect(x, y, qr_width, qr_height, fill=1, stroke=0)
                
                # 描画オブジェクトのスケーリング
                drawing.scale(self.scale_x, self.scale_y)
                
                # 描画
                drawing.drawOn(c, x, y)
                
                print("✅ QRコードの描画を完了")
            finally:
                c.restoreState()

        except Exception as e:
            print(f"⚠️ QRコードの配置に失敗しました: {e}")
            import traceback
            print("詳細なエラー情報:")
            print(traceback.format_exc()) 