from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.colors import CMYKColor

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
    c.setLineWidth(0.198)
    
    # キャンバスのサイズを取得
    canvas_width = c._pagesize[0]
    
    # ロゴの四隅の座標
    rect_corners = {
        'lt': {'x': logo_x - x, 'y': logo_y - y},
        'rt': {'x': logo_x - x + logo_width, 'y': logo_y - y},
        'lb': {'x': logo_x - x, 'y': logo_y - y + logo_height},
        'rb': {'x': logo_x - x + logo_width, 'y': logo_y - y + logo_height}
    }
    
    # パースペクティブグリッドの線を描画（オフセットを考慮）
    # 左側の線（上端）
    # 傾きを計算
    slope_lt = (y + rect_corners['lt']['y'] - y) / (x + rect_corners['lt']['x'] - x)
    # キャンバスの左端まで延長
    start_y_lt = y - slope_lt * x
    c.line(0, start_y_lt, x + rect_corners['lt']['x'], y + rect_corners['lt']['y'])
    
    # 左側の線（下端）
    slope_lb = (y + rect_corners['lb']['y'] - (y + height)) / (x + rect_corners['lb']['x'] - x)
    start_y_lb = (y + height) - slope_lb * x
    c.line(0, start_y_lb, x + rect_corners['lb']['x'], y + rect_corners['lb']['y'])
    
    # 右側の線（上端）
    slope_rt = (y + rect_corners['rt']['y'] - y) / (x + rect_corners['rt']['x'] - (x + width))
    end_y_rt = y + slope_rt * (canvas_width - (x + width))
    c.line(x + rect_corners['rt']['x'], y + rect_corners['rt']['y'], canvas_width, end_y_rt)
    
    # 右側の線（下端）
    slope_rb = (y + rect_corners['rb']['y'] - (y + height)) / (x + rect_corners['rb']['x'] - (x + width))
    end_y_rb = (y + height) + slope_rb * (canvas_width - (x + width))
    c.line(x + rect_corners['rb']['x'], y + rect_corners['rb']['y'], canvas_width, end_y_rb)
    
    # ロゴの位置に応じて追加の線を描画
    if height / 2 < logo_y + logo_height / 2:
        # ロゴが上半分にある場合
        # 右上から左上への線
        slope_lt2 = (y + rect_corners['lt']['y'] - y) / (x + rect_corners['lt']['x'] - (x + width))
        end_y_lt2 = y + slope_lt2 * (canvas_width - (x + width))
        c.line(x + rect_corners['lt']['x'], y + rect_corners['lt']['y'], canvas_width, end_y_lt2)
        
        # 左上から右上への線
        slope_rt2 = (y + rect_corners['rt']['y'] - y) / (x + rect_corners['rt']['x'] - x)
        start_y_rt2 = y - slope_rt2 * x
        c.line(0, start_y_rt2, x + rect_corners['rt']['x'], y + rect_corners['rt']['y'])
    else:
        # ロゴが下半分にある場合
        # 右下から左下への線
        slope_rb2 = (y + rect_corners['rb']['y'] - (y + height)) / (x + rect_corners['rb']['x'] - x)
        start_y_rb2 = (y + height) - slope_rb2 * x
        c.line(0, start_y_rb2, x + rect_corners['rb']['x'], y + rect_corners['rb']['y'])
        
        # 左下から右下への線
        slope_lb2 = (y + rect_corners['lb']['y'] - (y + height)) / (x + rect_corners['lb']['x'] - (x + width))
        end_y_lb2 = (y + height) + slope_lb2 * (canvas_width - (x + width))
        c.line(x + rect_corners['lb']['x'], y + rect_corners['lb']['y'], canvas_width, end_y_lb2)
    
    # ロゴの矩形を描画
    c.rect(logo_x, logo_y, logo_width, logo_height)

def draw_isolation_grid(c: canvas.Canvas, x: float, y: float, width: float, height: float,
                       logo_x: float, logo_y: float, logo_width: float, logo_height: float,
                       image_scale: float):
    """アイソレーショングリッドを描画"""
    # グリッドの線の色と太さを設定
    c.setStrokeColor(Color(0.4, 0.4, 0.4))  # グレー
    c.setLineWidth(0.198)
    
    # ロゴの四隅の座標
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
    # c.line(x + rect_corners['rt']['x'] + image_scale * -0.3, 0, x + rect_corners['rt']['x'] + image_scale * -0.3, canvas_height)

def draw_hybrid_grid(c: canvas.Canvas, x: float, y: float, width: float, height: float,
                    logo_x: float, logo_y: float, logo_width: float, logo_height: float,
                    unit_size: float):
    """ハイブリッド効果のあるグリッドを描画"""
    # グリッドの線の色と太さを設定（CMYKでK=70%）
    c.setStrokeColor(CMYKColor(0, 0, 0, 0.7))  # C=0%, M=0%, Y=0%, K=70%
    c.setLineWidth(0.198)
    
    # ロゴの四隅の座標（x, yからの相対位置に調整）
    rect_corners = {
        'lt': {'x': logo_x, 'y': logo_y + logo_height},
        'rt': {'x': logo_x + logo_width, 'y': logo_y + logo_height},
        'lb': {'x': logo_x, 'y': logo_y},
        'rb': {'x': logo_x + logo_width, 'y': logo_y}
    }

    canvas_width = c._pagesize[0]
    canvas_height = c._pagesize[1]
    
    # 左側の垂直線
    c.line(logo_x, 0, logo_x, canvas_height)
    
    # 右側の垂直線
    c.line(rect_corners['rt']['x'], 0, rect_corners['rt']['x'], canvas_height)
    
    # 上部の水平線
    c.line(0, rect_corners['rt']['y'], canvas_width, rect_corners['rt']['y'])
    
    # 下部の水平線
    c.line(0, rect_corners['rb']['y'], rect_corners['rb']['x'], rect_corners['rb']['y'])
    
    step = 1
    while step * unit_size < canvas_width - (rect_corners['rt']['x'] - x):
        current_x = rect_corners['rt']['x'] + step * unit_size
        c.line(current_x, 0, current_x, rect_corners['rt']['y'])
        step += 1
    
    step = 1
    while step * unit_size < rect_corners['rt']['y']:
        current_y = rect_corners['rt']['y'] - unit_size * step
        c.line(rect_corners['rt']['x'], current_y, rect_corners['rt']['x'] + width, current_y)
        step += 1