import xml.etree.ElementTree as ET

# 出力先のSVGファイル
output_file = "test_output.svg"
logo_path = "assets/DL_LOGO_HorizontalStacked_Black_CMYK.svg"

# 名刺サイズ
MEISHI_WIDTH = 266
MEISHI_HEIGHT = 164

# ロゴが収まる表示枠
LOGO_MAX_WIDTH = 100  # 横幅の最大値
LOGO_MAX_HEIGHT = 50  # 縦幅の最大値

def generate_svg_with_embedded_logo():
    # 1) メイン<svg> ルート要素を作成
    main_svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'width': str(MEISHI_WIDTH),
        'height': str(MEISHI_HEIGHT),
    })

    # 2) 背景用 <rect>
    ET.SubElement(main_svg, 'rect', {
        'x': '0',
        'y': '0',
        'width': str(MEISHI_WIDTH),
        'height': str(MEISHI_HEIGHT),
        'fill': 'white',
        'stroke': 'black'
    })

    # 3) ロゴSVGをパース
    logo_tree = ET.parse(logo_path)
    logo_root = logo_tree.getroot()

    # 4) ロゴの viewBox 取得（例: "0 0 677 398"）
    vb = logo_root.get('viewBox', '0 0 677 398').split()
    vb_width = float(vb[2])
    vb_height = float(vb[3])

    # 5) 縦横比を保つため、同じスケール値を使う
    scale = min(LOGO_MAX_WIDTH / vb_width, LOGO_MAX_HEIGHT / vb_height)

    # ロゴの実際の描画サイズ (比率維持後)
    real_w = vb_width * scale
    real_h = vb_height * scale

    # 6) ロゴを中央に配置
    logo_x = (MEISHI_WIDTH - real_w) / 2
    logo_y = (MEISHI_HEIGHT - real_h) / 2

    # 7) <g> で translate & scale
    group_elem = ET.SubElement(main_svg, 'g', {
        'transform': f"translate({logo_x},{logo_y}) scale({scale},{scale})"
    })

    # 8) ロゴの子要素を <g> にコピー（実体埋め込み）
    for child in list(logo_root):
        group_elem.append(child)

    # 9) <svg> をファイルへ書き出し
    tree = ET.ElementTree(main_svg)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"✅ SVG生成完了: {output_file}")

if __name__ == "__main__":
    generate_svg_with_embedded_logo()
