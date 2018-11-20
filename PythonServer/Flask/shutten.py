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
#過去に踏んだもののidを格納する
hist = []
#対応表
taio = [[1,3,4],[3,4,5],[1,4,5],[4,6,7],[6,7,8],[4,7,8]]

#はじめの３つのID
stat = [11,12,13,0,0,0,0,0,0]

send_u_array = ['']*9

def ser_to_unity(ser):
    #今踏まれたidを格納（ここがシリアルで受信したものになる)
    now_id = stat[int(ser.decode('utf-8'))]
        #unityに送る文字配列（長さ10）、毎回初期化
    send_u_array = ['']*9
    for i in book_array:
        send_u_array[i] =data["作品名"][i]
    print(send_u_array)
    print("stat=",stat)
    #    print(','.join(send_u_array))
    return ','.join(send_u_array)

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

ser = serial.Serial('/dev/cu.usbmodem1411',9600,timeout=0.2)

c = ""


# threading
def serT():
    global c
    prev_stat = ""

    while True:
        s = ser.readline().strip()
        if s!= prev_stat:
            c = ser_to_unity(s)
            print("c updated")
        else:
            print("same")
        prev_stat = s
        print(c)
        # c = ser.readline().decode('utf8').rstrip()

timer = threading.Timer(0.0, serT)

#flask初期化
app = Flask(__name__)
@app.route("/", methods=['GET'])
def index():
    # Add 1 second delay?
    global c
    return str(c)


    # Last working 2018/11/13
    # if cBefore != c:
    #     return c
    # else:
    #     return None
    # cBefore = c

    #str = ser()
#    if str=="26":
#        str = "a,a,a,a,a,a,a,a,a,a"
#   print("str=",str)
#return str
#    return main()


if __name__ == "__main__":
    timer.start()
    app.debug = True
    app.run()

