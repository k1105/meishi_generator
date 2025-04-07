from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Line, Drawing
from reportlab.graphics.renderPDF import draw
import math
from reportlab.lib.colors import Color

def draw_grid(c: canvas.Canvas, x: float, y: float, width: float, height: float, 
             unit_size: float, stroke_width: float = 0.3, stroke_color: tuple = (0.4, 0.4, 0.4)):
    """グリッドを描画する基本関数"""
    # グリッドの線の色と太さを設定
    c.setStrokeColorRGB(*stroke_color)
    c.setLineWidth(stroke_width)
    
    # 水平線を描画
    for i in range(int(height / unit_size) + 1):
        y_pos = y + i * unit_size
        c.line(x, y_pos, x + width, y_pos)
    
    # 垂直線を描画
    for i in range(int(width / unit_size) + 1):
        x_pos = x + i * unit_size
        c.line(x_pos, y, x_pos, y + height)

def draw_perspective_grid(c: canvas.Canvas, x: float, y: float, width: float, height: float,
                         logo_x: float, logo_y: float, logo_width: float, logo_height: float,
                         unit_size: float):
    """パースペクティブ効果のあるグリッドを描画"""
    # グリッドの線の色と太さを設定
    c.setStrokeColor(Color(0.4, 0.4, 0.4))  # グレー
    c.setLineWidth(0.3)
    
    # ロゴの四隅の座標（x, yからの相対位置に調整）
    rect_corners = {
        'lt': {'x': logo_x - x, 'y': logo_y - y},
        'rt': {'x': logo_x - x + logo_width, 'y': logo_y - y},
        'lb': {'x': logo_x - x, 'y': logo_y - y + logo_height},
        'rb': {'x': logo_x - x + logo_width, 'y': logo_y - y + logo_height}
    }
    
    # キャンバスのサイズを取得
    canvas_width = c._pagesize[0]
    canvas_height = c._pagesize[1]
    
    # パースペクティブグリッドの線を描画
    # 左側の線
    c.line(0, 0, x + rect_corners['lt']['x'], y + rect_corners['lt']['y'])
    c.line(0, height, x + rect_corners['lb']['x'], y + rect_corners['lb']['y'])
    
    # 右側の線
    c.line(width, 0, x + rect_corners['rt']['x'], y + rect_corners['rt']['y'])
    c.line(width, height, x + rect_corners['rb']['x'], y + rect_corners['rb']['y'])
    
    # ロゴの位置に応じて追加の線を描画
    if height / 2 < logo_y + logo_height / 2:
        # ロゴが上半分にある場合
        c.line(width, 0, x + rect_corners['lt']['x'], y + rect_corners['lt']['y'])
        c.line(0, 0, x + rect_corners['rt']['x'], y + rect_corners['rt']['y'])
    else:
        # ロゴが下半分にある場合
        c.line(0, height, x + rect_corners['rb']['x'], y + rect_corners['rb']['y'])
        c.line(width, height, x + rect_corners['lb']['x'], y + rect_corners['lb']['y'])
    
    # ロゴの矩形を描画
    c.rect(logo_x, logo_y, logo_width, logo_height)

def draw_isolation_grid(c: canvas.Canvas, x: float, y: float, width: float, height: float,
                       logo_x: float, logo_y: float, logo_width: float, logo_height: float,
                       image_scale: float):
    """アイソレーショングリッドを描画"""
    # グリッドの線の色と太さを設定
    c.setStrokeColor(Color(0.4, 0.4, 0.4))  # グレー
    c.setLineWidth(0.3)
    
    # ロゴの四隅の座標（x, yからの相対位置に調整）
    rect_corners = {
        'lt': {'x': logo_x - x, 'y': logo_y - y},
        'rt': {'x': logo_x - x + logo_width, 'y': logo_y - y},
        'lb': {'x': logo_x - x, 'y': logo_y - y + logo_height},
        'rb': {'x': logo_x - x + logo_width, 'y': logo_y - y + logo_height}
    }
    
    # キャンバスのサイズを取得
    canvas_width = c._pagesize[0]
    canvas_height = c._pagesize[1]
    
    # 水平線を描画（下部）
    c.line(0, y + rect_corners['lb']['y'] + image_scale * -0.3, canvas_width, y + rect_corners['lb']['y'] + image_scale * -0.3)
    c.line(0, y + rect_corners['lb']['y'] + image_scale * -4.7, canvas_width, y + rect_corners['lb']['y'] + image_scale * -4.7)
    c.line(0, y + rect_corners['lb']['y'] + image_scale * -9.1, canvas_width, y + rect_corners['lb']['y'] + image_scale * -9.1)
    
    # 水平線を描画（上部）
    c.line(0, y + rect_corners['lt']['y'] + image_scale * 0.3, canvas_width, y + rect_corners['lt']['y'] + image_scale * 0.3)
    c.line(0, y + rect_corners['lt']['y'] + image_scale * 4.7, canvas_width, y + rect_corners['lt']['y'] + image_scale * 4.7)
    c.line(0, y + rect_corners['lt']['y'] + image_scale * 9.1, canvas_width, y + rect_corners['lt']['y'] + image_scale * 9.1)
    
    # 垂直線を描画（左部）
    c.line(x + rect_corners['lt']['x'] + image_scale * 0.3, 0, x + rect_corners['lt']['x'] + image_scale * 0.3, canvas_height)
    c.line(x + rect_corners['lt']['x'] + image_scale * 4.7, 0, x + rect_corners['lt']['x'] + image_scale * 4.7, canvas_height)
    c.line(x + rect_corners['lt']['x'] + image_scale * 9.1, 0, x + rect_corners['lt']['x'] + image_scale * 9.1, canvas_height)
    
    # 垂直線を描画（右部）
    c.line(x + rect_corners['rt']['x'] + image_scale * -9.1, 0, x + rect_corners['rt']['x'] + image_scale * -9.1, canvas_height)
    c.line(x + rect_corners['rt']['x'] + image_scale * -4.7, 0, x + rect_corners['rt']['x'] + image_scale * -4.7, canvas_height)
    c.line(x + rect_corners['rt']['x'] + image_scale * -0.3, 0, x + rect_corners['rt']['x'] + image_scale * -0.3, canvas_height)

def draw_hybrid_grid(c: canvas.Canvas, x: float, y: float, width: float, height: float,
                    logo_x: float, logo_y: float, logo_width: float, logo_height: float,
                    unit_size: float):
    """ハイブリッド効果のあるグリッドを描画"""
    # グリッドの線の色と太さを設定
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    c.setLineWidth(0.3)
    
    # ロゴの中心点
    logo_center_x = logo_x + logo_width / 2
    logo_center_y = logo_y + logo_height / 2
    
    # グリッドの密度を調整
    density = 2
    adjusted_unit_size = unit_size * density
    
    # パースペクティブグリッドを描画
    draw_perspective_grid(c, x, y, width, height, logo_x, logo_y, logo_width, logo_height, unit_size)
    
    # アイソレーショングリッドを部分的に描画
    num_lines = 8  # 放射状の線の数
    for i in range(num_lines):
        angle = (2 * math.pi * i) / num_lines
        # 放射状の線を描画（短めに）
        start_x = logo_center_x
        start_y = logo_center_y
        end_x = start_x + math.cos(angle) * (width / 3)
        end_y = start_y + math.sin(angle) * (height / 3)
        c.line(start_x, start_y, end_x, end_y)
    
    # 同心円状のグリッドを部分的に描画
    num_circles = 3
    for i in range(1, num_circles + 1):
        radius = i * adjusted_unit_size * 2
        c.circle(logo_center_x, logo_center_y, radius) 