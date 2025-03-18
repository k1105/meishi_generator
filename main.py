
import argparse
import os
import datetime
import svgwrite
import xml.etree.ElementTree as ET

# コマンドライン引数を受け取る
parser = argparse.ArgumentParser()
parser.add_argument("--img", required=True, help="画像のパス")
parser.add_argument("--question", default="あなたの好きな作品やデザインを教えてください。", help="質問文")
parser.add_argument("--num", type=int, default=3, help="生成する数")
args = parser.parse_args()

# タイムスタンプ付きの出力ディレクトリ
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"./out/{timestamp}"
svg_dir = os.path.join(output_dir, "svg")
os.makedirs(svg_dir, exist_ok=True)

# 名刺のサイズ
MEISHI_WIDTH = 266
MEISHI_HEIGHT = 164

# サイズリスト（ロゴサイズの定義）
SIZE_LIST = {
    "xl": 3,
    "l": 2.5,
    "m": 1.5,
    "s": 1,
    "xs": 0.5,
}

# デフォルトの入力データ
PATTERN_DATA = {
    "position": {"x": 100, "y": 100},
    "size": "m",
    "grid": {"type": "perspective", "detailedness": 10},
}

LOGO_PATH = "assets/DL_LOGO_HorizontalStacked_Black_CMYK.svg"


def draw_meishi_svg(output_path, pattern_data):
    """
    1) svgwrite で一時SVGを作り、グリッド描画
    2) 生成した一時SVGを ElementTree で読み込み
    3) ロゴSVGを読み込み、<g>として挿入
    4) 最終的なSVGを output_path に保存
    """
    # 一時SVGファイルのパス
    temp_svg_path = os.path.splitext(output_path)[0] + "_temp.svg"

    # -----------------------------
    # (1) svgwriteでメインSVGを作る
    # -----------------------------
    dwg = svgwrite.Drawing(temp_svg_path, size=(MEISHI_WIDTH, MEISHI_HEIGHT))

    position = pattern_data["position"]
    size = pattern_data["size"]
    grid = pattern_data["grid"]
    grid_type = grid["type"]
    detailedness = grid["detailedness"]

    # 背景を描画 (白ベタ)
    dwg.add(dwg.rect(insert=(0, 0), size=(MEISHI_WIDTH, MEISHI_HEIGHT), fill="white"))

    # ロゴ表示サイズ
    scale = SIZE_LIST.get(size, 1)
    logo_width = int(50 * scale)
    logo_height = int(30 * scale)

    # ロゴの位置 (p5.js 相当)
    image_x = position["x"] - logo_width // 2
    image_y = position["y"] - logo_height // 2

    rect_corners = {
        "lt": {"x": image_x, "y": image_y},
        "lb": {"x": image_x, "y": image_y + logo_height},
        "rt": {"x": image_x + logo_width, "y": image_y},
        "rb": {"x": image_x + logo_width, "y": image_y + logo_height},
    }

    # グリッド描画
    if grid_type == "perspective":
        dwg.add(dwg.line(start=(0, 0), end=(rect_corners["lt"]["x"], rect_corners["lt"]["y"]), stroke="gray"))
        dwg.add(dwg.line(start=(0, 0), end=(rect_corners["rt"]["x"], rect_corners["rt"]["y"]), stroke="gray"))
        dwg.add(dwg.line(start=(MEISHI_WIDTH, 0), end=(rect_corners["lt"]["x"], rect_corners["lt"]["y"]), stroke="gray"))
        dwg.add(dwg.line(start=(0, MEISHI_HEIGHT), end=(rect_corners["lb"]["x"], rect_corners["lb"]["y"]), stroke="gray"))
        dwg.add(dwg.line(start=(MEISHI_WIDTH, 0), end=(rect_corners["rt"]["x"], rect_corners["rt"]["y"]), stroke="gray"))
        dwg.add(dwg.line(start=(MEISHI_WIDTH, MEISHI_HEIGHT), end=(rect_corners["rb"]["x"], rect_corners["rb"]["y"]), stroke="gray"))

        # ロゴ部分の枠を描画
        dwg.add(dwg.rect(insert=(image_x, image_y), size=(logo_width, logo_height), stroke="gray", fill="none"))

    elif grid_type == "isolation":
        offsets = [-6.9, -3.4, 0.1]
        for offset in offsets:
            y_pos = rect_corners["lb"]["y"] + scale * offset
            dwg.add(dwg.line(start=(0, y_pos), end=(MEISHI_WIDTH, y_pos), stroke="gray"))

        for offset in offsets:
            y_pos = rect_corners["lt"]["y"] - scale * offset
            dwg.add(dwg.line(start=(0, y_pos), end=(MEISHI_WIDTH, y_pos), stroke="gray"))

        for offset in offsets:
            x_pos = rect_corners["lt"]["x"] - scale * offset
            dwg.add(dwg.line(start=(x_pos, 0), end=(x_pos, MEISHI_HEIGHT), stroke="gray"))

        for offset in offsets:
            x_pos = rect_corners["rt"]["x"] + scale * offset
            dwg.add(dwg.line(start=(x_pos, 0), end=(x_pos, MEISHI_HEIGHT), stroke="gray"))

    elif grid_type == "hybrid":
        # 垂直線
        dwg.add(dwg.line(start=(rect_corners["lt"]["x"], 0), end=(rect_corners["lt"]["x"], MEISHI_HEIGHT), stroke="gray"))
        dwg.add(dwg.line(start=(rect_corners["rt"]["x"], 0), end=(rect_corners["rt"]["x"], MEISHI_HEIGHT), stroke="gray"))

        # 水平線
        dwg.add(dwg.line(start=(0, rect_corners["rt"]["y"]), end=(MEISHI_WIDTH, rect_corners["rt"]["y"]), stroke="gray"))
        dwg.add(dwg.line(start=(0, rect_corners["rb"]["y"]), end=(rect_corners["rb"]["x"], rect_corners["rb"]["y"]), stroke="gray"))

        # グリッドの単位サイズ計算
        unit_size = (MEISHI_WIDTH - rect_corners["rt"]["x"]) / (2 * detailedness)

        if unit_size > 0:
            step = 1
            x_pos = rect_corners["rt"]["x"]
            while step * unit_size < MEISHI_WIDTH - rect_corners["rt"]["x"]:
                x_pos += unit_size
                dwg.add(dwg.line(start=(x_pos, rect_corners["rt"]["y"]), end=(x_pos, MEISHI_HEIGHT), stroke="gray"))
                step += 1

            step = 1
            y_pos = rect_corners["rt"]["y"]
            while step * unit_size < MEISHI_HEIGHT - rect_corners["rt"]["y"]:
                y_pos += unit_size
                dwg.add(dwg.line(start=(rect_corners["rt"]["x"], y_pos), end=(MEISHI_WIDTH, y_pos), stroke="gray"))
                step += 1
    # ここではロゴをまだ貼り付けない（svgwriteで外部SVG埋め込みが難しいため）
    # 一旦グリッドだけで保存
    dwg.save()

    # -----------------------------------------
    # (2) temp_svg_path を ElementTree でパース
    # -----------------------------------------
    try:
        main_tree = ET.parse(temp_svg_path)
        main_root = main_tree.getroot()
    except Exception as e:
        print(f"⚠️ ElementTree parse error: {e}")
        return

    # ------------------------------------
    # (3) ロゴSVGを読み込み、<g>に挿入する
    # ------------------------------------
    try:
        logo_tree = ET.parse(LOGO_PATH)
        logo_root = logo_tree.getroot()

        # ロゴの viewBox 例: "0 0 677 398"
        vb = logo_root.get('viewBox', '0 0 677 398').split()
        vb_width = float(vb[2])
        vb_height = float(vb[3])

        # 同じ比率でスケール
        # → 今回はユーザー指定の 50*scale, 30*scale を使うため、
        #    縦横別々にscale。アスペクト崩れるかも → 気になるならmin()で統一
        scale_x = logo_width / vb_width
        scale_y = logo_height / vb_height

        # <g> でtranslate & scale
        group_elem = ET.SubElement(
            main_root,
            'g',
            {
                'transform': f"translate({image_x},{image_y}) scale({scale_x},{scale_y})"
            }
        )

        # ロゴの子要素をコピー (実体埋め込み)
        for child in list(logo_root):
            group_elem.append(child)

    except Exception as e:
        print(f"⚠️ ロゴ埋め込みエラー: {e}")

    # -----------------------------------
    # (4) 最終的なSVGを output_path に保存
    # -----------------------------------
    main_tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ SVGを生成: {output_path}")

    os.remove(temp_svg_path)

# `num` 回分のSVG名刺を生成
if __name__ == "__main__":
    for i in range(1, args.num + 1):
        svg_output_file = os.path.join(svg_dir, f"{i:02}.svg")
        draw_meishi_svg(svg_output_file, PATTERN_DATA)
