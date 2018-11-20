# coding: utf-8
from PIL import Image
from function import draw_text
import sys

############################ Strat 各変数の宣言

# 引数から文字を受け取る
#TARGET_STRING = sys.argv[1]
TARGET_STRING_1 = "吾輩は猫である    「吾輩は猫である」  夏目漱石"
TARGET_STRING_2 = "飛び降りて 「銀河鉄道のよる」   宮沢賢治"

# otfファイルまでのパス
OTF_FILE_PATH = 'tate_test.otf'

# 出力用ファイルまでのパス
OUTPUT_FILE_PATH = 'output.jpg'

# 元画像ファイルまでのパス
FRAME_FILE_PATH  = 'image.jpg'

############################ End 各変数の宣言

# 元画像データを取得
image_data = Image.open(FRAME_FILE_PATH)

# 文字合成
font_size          = 6
draw_start_x       = 10
draw_start_y       = 10
draw_text(image_data, font_size, OTF_FILE_PATH, TARGET_STRING_1, draw_start_x, draw_start_y,"#000000")
draw_text(image_data, font_size, OTF_FILE_PATH, TARGET_STRING_2, draw_start_x+10, draw_start_y,"#000000")

# 合成した画像の書き出し
image_data.save(OUTPUT_FILE_PATH)
image_data.show();
