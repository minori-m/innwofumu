# coding: utf-8
from PIL import ImageFont, ImageDraw

def draw_text(frame_image, font_size, font_file_path, target_string, draw_start_x, draw_start_y, font_color='#ffffff'):
    """
        テキストの縦書き描画
        :param frame_image        Image:  フレームのImageオブジェクト
        :param font_size          int:    フォントサイズ
        :param font_file_path     string: OTFファイルまでのパス
        :param target_string      string: 対象の文字列
        :param draw_start_x       int:    描画開始位置_X
        :param draw_start_y       int:    描画開始位置_Y
        :param font_color         string: 描画する文字の色 (デフォルト: "#000000")
        """
    
    # 描画用データを取得
    draw = ImageDraw.Draw(frame_image)
    
    # フォントデータを取得
    image_font = ImageFont.truetype(font_file_path, font_size)
    
    # 各文字の描画管理変数
    ix, iy = 0, 0
    
    for c in target_string:
        x = draw_start_x - ix * font_size
        y = draw_start_y + (iy * font_size)
        
        # 今回描画する1文字の詳細なX, Yを設定
        char_width, char_height = image_font.getsize(c)
        x += (font_size - char_width) / 2
        y += draw_start_y
        
        # 指定の場所へ文字を描画
        draw.text((x, y), c, font=image_font, fill=font_color)
        
        # 次の文字へ
        iy += 1
    
    return True
