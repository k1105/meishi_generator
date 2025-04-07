import argparse
import os
import json
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from meishi_back import create_back_design


def generate_meishi_back(data: dict, output_path: str):
    """名刺の裏面を生成"""
    try:
        # 名刺サイズ（91mm × 55mm）
        width_mm = 91
        height_mm = 55
        width_pt, height_pt = width_mm * mm, height_mm * mm

        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # PDFの設定
        c = canvas.Canvas(
            output_path,
            pagesize=(width_pt + 6 * mm, height_pt + 6 * mm),
            pageCompression=1,  # 圧縮を有効化
            invariant=True,  # 再現性を確保
            enforceColorSpace='rgb',  # カラースペースをRGBに固定
            pdfVersion=(1, 4)  # PDFバージョンを1.4に固定（タプル形式で指定）
        )

        # 裏面を生成
        grid_type = data.get("pattern", {}).get("grid", {}).get("type", "isolation")
        back_design = create_back_design(grid_type)
        back_design._generate_design(c, data)

        # PDFを保存
        c.save()
        print(f"✅ 名刺の裏面を生成しました: {output_path}")

    except Exception as e:
        print(f"⚠️ 名刺の裏面の生成に失敗しました: {e}")
        import traceback
        print("詳細なエラー情報:")
        print(traceback.format_exc())


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
    pdf_filename = f"{employee_number}_{name_safe}_back.pdf"
    folder_path = os.path.dirname(json_path)
    pdf_path = os.path.join(folder_path, "pdf", pdf_filename)

    generate_meishi_back(data, pdf_path)


if __name__ == "__main__":
    main()
