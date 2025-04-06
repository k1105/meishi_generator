import argparse
import os
import json
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas

from meishi_front import MeishiFront
from meishi_back import create_back_design


def generate_meishi_pdf(data: dict, output_path: str):
    # 名刺サイズ（91mm × 55mm）
    width_mm = 91
    height_mm = 55
    width_pt, height_pt = width_mm * mm, height_mm * mm

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # PDFの設定
    c = canvas.Canvas(
        output_path,
        pagesize=(width_pt, height_pt),
        pageCompression=1,  # 圧縮を有効化
        invariant=True  # 再現性を確保
    )

    # 表面を生成
    front_design = MeishiFront(width_mm, height_mm)
    front_design._generate_design(c, data)
    c.showPage()

    # 裏面を生成
    grid_type = data.get("grid", {}).get("type", "isolation")
    back_design = create_back_design(grid_type)
    back_design._generate_design(c, data)

    # PDFを保存
    c.save()
    print(f"✅ 名刺PDFを生成しました: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="名刺データのJSONファイルパス")
    args = parser.parse_args()

    json_path = args.json
    if not os.path.exists(json_path):
        print(f"❌ JSONファイルが見つかりません: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    employee_number = data.get("employeeNumber", "unknown")
    name_safe = data.get("name", "noname").lower().replace(" ", "_")
    pdf_filename = f"{employee_number}_{name_safe}.pdf"
    folder_path = os.path.dirname(json_path)
    pdf_path = os.path.join(folder_path, pdf_filename)

    generate_meishi_pdf(data, pdf_path)


if __name__ == "__main__":
    main()
