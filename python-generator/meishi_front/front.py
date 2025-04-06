import os
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from meishi_front.design import FrontDesign
from meishi_front.qr_placement import QRPlacement


class MeishiFront:
    def __init__(self, width_mm=91, height_mm=55):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.width_pt = width_mm * mm
        self.height_pt = height_mm * mm

        # フォントファイルの登録
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_dir = os.path.join(base_dir, "fonts")
        print(f"📁 フォントディレクトリ: {font_dir}")

        self.fonts = {
            "ja": {
                "name": "NotoSansJP-Bold",
                "path": os.path.join(font_dir, "NotoSansJP-Bold.ttf")
            },
            "en": {
                "name": "Inter-Bold",
                "path": os.path.join(font_dir, "Inter_18pt-Bold.ttf")
            },
            "mono": {
                "name": "IBMPlexMono",
                "path": os.path.join(font_dir, "IBMPlexMono-Regular.ttf")
            }
        }

        # フォントファイルの存在確認と登録
        for font in self.fonts.values():
            print(f"\n🔍 フォント確認: {font['name']}")
            print(f"📄 パス: {font['path']}")
            
            if not os.path.exists(font["path"]):
                print(f"⚠️ フォントファイルが見つかりません: {font['path']}")
                continue
            
            try:
                print(f"📝 フォントを登録中: {font['name']}")
                pdfmetrics.registerFont(TTFont(font["name"], font["path"]))
                print(f"✅ フォントを登録しました: {font['name']}")
            except Exception as e:
                print(f"⚠️ フォントの登録に失敗しました ({font['name']}): {str(e)}")
                import traceback
                print("詳細なエラー情報:")
                print(traceback.format_exc())

        # デザインコンポーネントの初期化
        self.main_design = FrontDesign(width_mm, height_mm)
        self.qr_placement = QRPlacement(width_mm, height_mm)

    def generate(self, output_path: str, data: dict):
        """名刺の表面を生成"""
        try:
            # 出力ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # PDFの設定
            c = canvas.Canvas(
                output_path,
                pagesize=(self.width_pt, self.height_pt),
                pageCompression=1,  # 圧縮を有効化
                invariant=True,  # 再現性を確保
                enforceColorSpace='rgb',  # カラースペースをRGBに固定
                pdfVersion='1.4'  # PDFバージョンを1.4に固定
            )

            # デザインの生成
            self._generate_design(c, data)

            # PDFを保存
            c.save()
            print(f"✅ 名刺の表面を生成しました: {output_path}")

        except Exception as e:
            print(f"⚠️ 名刺の表面の生成に失敗しました: {e}")
            import traceback
            print("詳細なエラー情報:")
            print(traceback.format_exc())

    def _generate_design(self, c: canvas.Canvas, data: dict):
        """名刺の表面デザインを生成"""
        # メインデザインの生成
        self.main_design.generate(c, data)

        # QRコードの配置
        self.qr_placement.place(c)
