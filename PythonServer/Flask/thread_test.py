# python
#coding:utf-8
import serial
import re
from flask import Flask
#import data_refine
import pandas as pd
from mutagen.mp3 import MP3 as mp3
import pygame
import time
import random
import threading

flag = 0

#csvを読んでdfにする
def csv_to_df(path):
    data = pd.read_csv(path)
    return data

#音声ファイルを再生する
def read_aloud(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename) #音源を読み込み
    mp3_length = mp3(filename).info.length #音源の長さ取得
    pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
    time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
    pygame.mixer.music.stop() #音源の長さ待ったら再生停止


#setup関数
#韻の表読み込み
data = csv_to_df("in_data.csv")
#    print(data)
#列の定義
colnum_same_id = 5
#    print(data["呼応するもの"])
colnum_similar_id = 6
#過去に踏んだもののidを格納する
hist = []

#以下main
send = "a,a,a,a,a,a,a,a,a,a"

def ser():
    with serial.Serial('/dev/cu.usbmodem1411',9600) as ser:
        while True:
            print("True loop")
            c = ser.readline().decode('utf8').rstrip()
            if len(c)>0:
                print(c)
#                app.debug = True
#                app.run()

                send = c
                return c
#                if flag == 0:
#                    read_aloud("voices/Indigo.mp3")
#                    flag = 1
#                    print("flag=",flag)
#                elif flag == 1:
#                    pygame.mixer.music.stop() #音源の長さ待ったら再生停止
#                    flag = 0
#                    print("flag=",flag)

        ser.close()

#ser = serial.Serial('/dev/cu.usbmodem1411',9600,timeout=0.2)

#flask初期化
app = Flask(__name__)
@app.route("/", methods=['GET'])
def index():
#    cBefore = ""
#    #print("True loop")
#    c = ser.readline().decode('utf8').rstrip()
#    # Make a script that checks the size. Make a filter
#    if cBefore != c:
#        return c
#    else:
#        return None
#    cBefore = c

    str = ser()
#    if str=="26":
#    str = "a,a,a,a,a,a,a,a,a,a"
#   print("str=",str)
    return str
#    return main()


if __name__ == "__main__":
    app.debug = True
    app.run()

