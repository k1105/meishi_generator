from reportlab.pdfgen import canvas
from reportlab.graphics.renderPDF import draw
from svglib.svglib import svg2rlg, Drawing
import os
from typing import Tuple
from reportlab.lib.colors import CMYKColor


class BaseBackDesign:
    def __init__(self, width_mm=91, height_mm=55):
        # 名刺のサイズに周囲3mmを足した大きさ
        self.width_mm = width_mm + 6  # 左右3mmずつ
        self.height_mm = height_mm + 6  # 上下3mmずつ
        self.minimum_grid_size = 4.96  # px単位
        self.max_grid_size = self.minimum_grid_size * 4

    def calculate_logo_size(self, data: dict) -> Tuple[float, float]:
        """ロゴのサイズを計算"""
        # ロゴのパスを取得
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "DL_LOGO_HorizontalStacked_Black_CMYK.svg")
        
        # サイズリスト（ロゴサイズの定義）
        size_list = {
            "l": self.max_grid_size * 5,
            "m": self.max_grid_size * 4,
            "s": self.max_grid_size * 3,
            "xs": self.max_grid_size * 2,
        }
        
        # patternオブジェクトからsizeを取得
        target_size = size_list.get(data.get("pattern", {}).get("size", "m"), size_list["m"])
        
        # SVGファイルからロゴのアスペクト比を取得
        with open(logo_path, 'r') as f:
            svg_content = f.read()
            # viewBox属性からアスペクト比を取得
            import re
            viewbox_match = re.search(r'viewBox="([^"]*)"', svg_content)
            if viewbox_match:
                viewbox = viewbox_match.group(1).split()
                if len(viewbox) >= 4:
                    svg_width = float(viewbox[2])
                    svg_height = float(viewbox[3])
                    aspect_ratio = svg_width / svg_height
                else:
                    aspect_ratio = 2.5  # デフォルト値
            else:
                aspect_ratio = 2.5  # デフォルト値
        
        # アスペクト比を維持して幅を計算
        height_px = target_size
        width_px = height_px * aspect_ratio
        
        return width_px, height_px

    def calculate_logo_position(self, data: dict, logo_width: float, logo_height: float) -> Tuple[float, float]:
        """ロゴの位置を計算"""
        # オフセットを計算（px単位）
        offset = 22.5922
        
        # 名刺のサイズを計算（px単位）
        meishi_width = 257.95
        meishi_height = 155.91
        
        # patternオブジェクトからpositionを取得
        position = data.get("pattern", {}).get("position", {"x": 50, "y": 50})  # デフォルトは中央
        
        # 位置を計算（フロントエンドと同じ計算式）
        x = offset + (meishi_width - offset * 2 - logo_width) * position["x"] / 100
        # Y座標を反転（フロントエンドの座標系に合わせる）
        y = meishi_height - (offset + (meishi_height - offset * 2 - logo_height) * position["y"] / 100) - logo_height
        
        # グリッドに合わせて位置を調整
        unit_size = self.minimum_grid_size
        x = int(x / unit_size) * unit_size
        y = int(y / unit_size) * unit_size
        
        return x, y

    def draw_logo(self, c: canvas.Canvas, logo_path: str, x: float, y: float, width: float, height: float):
        """共通のロゴ描画処理"""
        try:
            drawing = self._load_logo(logo_path)

            # 指定されたサイズに合わせてスケーリング
            scale_x = width / drawing.width
            scale_y = height / drawing.height
            scale = min(scale_x, scale_y)

            drawing.scale(scale, scale)

            # 指定された位置に描画
            draw(drawing, c, x, y)
        except Exception as e:
            print(f"⚠️ SVGロゴの描画中にエラーが発生しました: {e}")

    def _load_logo(self, logo_path: str) -> Drawing:
        """ロゴを読み込む"""
        try:
            # SVGファイルを読み込む
            drawing = svg2rlg(logo_path)
            return drawing
        except Exception as e:
            raise ValueError(f"ロゴの読み込みに失敗しました: {str(e)}")

    def generate(self, output_path: str, data: dict):
        """サブクラスで実装する必要があるメソッド"""
        try:
            # 出力ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # PDFの設定（mmをptに変換して設定）
            c = canvas.Canvas(
                output_path,
                pagesize=(self.width_mm * 2.8346, self.height_mm * 2.8346),  # 1mm = 2.8346pt
                pageCompression=1,  # 圧縮を有効化
                invariant=True,  # 再現性を確保
                colorSpace='RGB'  # カラースペースをRGBに設定
            )

            # デザインの生成
            self._generate_design(c, data)

            # PDFを保存
            c.save()
            
            # PDFをCMYKに変換
            from PyPDF2 import PdfReader, PdfWriter
            reader = PdfReader(output_path)
            writer = PdfWriter()
            
            # 各ページをCMYKに変換
            for page in reader.pages:
                writer.add_page(page)
            
            # CMYKプロファイルを設定
            writer.add_metadata({
                '/OutputIntents': [{
                    '/Type': '/OutputIntent',
                    '/S': '/GTS_PDFA1',
                    '/OutputCondition': 'sRGB IEC61966-2.1',
                    '/OutputConditionIdentifier': 'sRGB IEC61966-2.1',
                    '/RegistryName': 'http://www.color.org',
                    '/Info': 'sRGB IEC61966-2.1',
                    '/DestOutputProfile': 'sRGB IEC61966-2.1'
                }]
            })
            
            # 変換したPDFを保存
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            print(f"✅ 名刺の裏面を生成しました: {output_path}")

        except Exception as e:
            print(f"⚠️ 名刺の裏面の生成に失敗しました: {e}")
            import traceback
            print("詳細なエラー情報:")
            print(traceback.format_exc())

    def _generate_design(self, c: canvas.Canvas, data: dict):
        """サブクラスで実装する必要があるメソッド"""
        raise NotImplementedError("Subclasses must implement _generate_design()")
