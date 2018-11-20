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
import os

flag = 0

#csvを読んでdfにする
def csv_to_df(path):
    data = pd.read_csv(path)
    return data

#音声ファイルを再生する
def read_aloud(filename):
    pygame.mixer.init()
#    print("init")
    pygame.mixer.music.load(filename) #音源を読み込み
    mp3_length = mp3(filename).info.length #音源の長さ取得
    pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
#    print("play")
    time.sleep(mp3_length + 0.01) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
    pygame.mixer.music.stop() #音源の長さ待ったら再生停止
#    print("stopf")


#setup関数
#韻の表読み込み
data = csv_to_df("in_data.csv")
#過去に踏んだもののidを格納する
hist = []
#対応表
taio = [[1,3,4],[3,4,5],[1,4,5],[4,6,7],[6,7,8],[4,7,8]]

#はじめの３つのID
stat = [11,12,13,0,0,0,0,0,0]
#stat = [11,12,13,14,15,16,17,18,19]


#音源のpath
main_path = os.path.dirname(os.path.abspath( __file__ ))
file_path = os.path.join(main_path, "voices")


#unityに送る文字列の初期値
shoki = ['']*9
for i in range(len(stat)):
    if stat[i]!=0:
        shoki[i] = data["フレーズ"][stat[i]]
shoki = ','.join(shoki)

send_u_array = ['']*9

global num_funda
num_funda=0

def ser_to_unity(ser):
    global num_funda
    #今踏まれたidを格納（ここがシリアルで受信したものになる)
    print("strip=",ser.decode('utf-8'))
#    print("test=",stat[0]
    if len(ser.decode('utf-8'))>0:
        if num_funda<3:
            num_funda = num_funda + 1
            print("num_funda = ",num_funda)
            if num_funda == 3:
                print("hist_array=",hist)
                file_path_2 = os.path.join(file_path,data["ongen"][int(stat[int(ser.decode('utf-8'))])-1])
                read_aloud(file_path_2)

                num_funda = 0
                hist.clear()
                print("reseted")
                c=shoki
                return c
            now_id = stat[int(ser.decode('utf-8'))]
            print(now_id)
            #以下繰り返し
            #Arduinoから[これからひらくもの、...]の配列を受け取る（、これから出す文字列をdfから取り出す）
            book_array = taio[int(ser.decode('utf-8'))]
            #    now_id = book_array[0]
            print("now id:",now_id,type(now_id))
            hist.append(now_id)
            #Arduinoから読み取った値の音声データを今まで読んでいた音声データの末尾に付け加えて再生する histをread_aloudする的な
            #unityに送る文字配列（長さ10）、毎回初期化
            send_u_array = ['']*9
            #次に開く位置(Arduinoから送られてきたint列の1番目のセル以降）aをうけとり、Unityに送るchar列a番目に次に使うお文字列の1つをいれる（開かない場所はNaNか0)
#            print("ichibu=",data["一部一致"][int(now_id)])
            #    print(int(random.sample(data["完全一致"][int(now_id)].split(','),2)[0]))
            print(book_array[1])
            
                        #再生
            if num_funda == 1:
                file_path_2 = os.path.join(file_path,data["ongen"][int(now_id)])
            
            else:
                file_path_2 = os.path.join(file_path,data["ongen"][int(now_id)-1])
            
            read_aloud(file_path_2)

            
            same = data["完全一致"][int(now_id)-1].split(',')
            similar = data["一部一致"][int(now_id)-1].split(',')
            same.extend(similar)
            same_del = [i for i in same if i not in hist]
            print(same_del)
            same_del =list(filter(lambda str:str != '', same_del))
            print("same_del=" ,same_del)
            j=0
            ran_array = random.sample(same_del,3)
            for i in book_array:
                ran = int(ran_array[j])
                print("ran=",ran)
                j=j+1
                stat[i] = ran
                send_u_array[i] =data["フレーズ"][ran-1]
            print(send_u_array)
            print("stat=",stat)
            #    print(','.join(send_u_array))

        return ','.join(send_u_array)

def ser():
    with serial.Serial('/dev/cu.usbmodem1411',9600) as ser:
#    with serial.Serial('/dev/cu.wchusbserial1410',9600) as ser:
        while True:
            print("True loop")
            c = ser.readline().decode('utf8').rstrip()
            if len(c)>0:
                print(c)
#                app.debug = True
#                app.run()

                send = c
                return c
        ser.close()

ser = serial.Serial('/dev/cu.usbmodem1411',9600,timeout=0.2)



# threading
def serT():
    global c
    prev_stat = ""
    c=shoki
    while True:
        s = ser.readline().strip()
#        if len(s)>0 and s!= prev_stat and stat[int(ser.decode('utf-8'))] != 0:
        if len(s)>0 and s!= prev_stat:
            c = ser_to_unity(s)
#            print("oto=",data["ongen"][int(s.decode('utf-8'))-1])

            print("c updated")
        else:
            print("same")
        prev_stat = s

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



if __name__ == "__main__":
    timer.start()
    app.debug = True
    app.run()

