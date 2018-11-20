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
import os

import subprocess

#subprocess.call("aplay a.wav", shell=True)

send_u_array = ['']*10
ex_id_array=[11,12,13,14,15,16,17,18,19]
hist_array=[]


#csvを読んでdfにする
def csv_to_df(path):
    data = pd.read_csv(path)
    return data


#韻の表読み込み
data = csv_to_df("in_data.csv")
print(data)



#音声ファイルを再生する
def read_aloud(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename) #音源を読み込み
    mp3_length = mp3(filename).info.length #音源の長さ取得
    pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
    time.sleep(mp3_length+0.05) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
    pygame.mixer.music.stop() #音源の長さ待ったら再生停止
    print(filename," played")


#arduinoからのシリアル通信で値を読み取ってstrで返す
def ser():
    prev = 0
    main_path = os.path.dirname(os.path.abspath( __file__ ))
    file_path = os.path.join(main_path, "voices")

    with serial.Serial('/dev/cu.usbmodem1411',9600) as ser:
        #int配列の0番目が踏まれたもの、1番目以降が開くもの
        while True:
            print("True loop")
            c = ser.readline().decode('utf8').rstrip()
            print("c=",c)
            if prev == c:
                print("same")
            if len(c)>0 and prev != c:
#                if pygame.mixer.get_busy==True:
#                    pygame.mixer.music.fadeout(0.5)
                print("music loop")
                hist_array.append(c)
                print(hist_array)
                file_path_2 = os.path.join(file_path,data["ongen"][ex_id_array[int(c)-1]])
                read_aloud(file_path_2)
#                for j in reversed(hist_array):
#                    if int(j) == 0:
#                        file_path_2 = os.path.join(file_path,data["ongen"][ex_id_array[int(j)-1]])
#
#                    file_path_2 = os.path.join(file_path,data["ongen"][ex_id_array[int(j)]-1])
#                    read_aloud(file_path_2)
#                        print(c)
                #read_aloud(data)
            prev = c
            if len(hist_array)>2:
#                print("fin")
#                for j in reversed(hist_array):
#                    file_path_2 = os.path.join(file_path,data["ongen"][ex_id_array[int(j)-1]-1])
#                    read_aloud(file_path_2)
                hist_array.clear()
#                read_aloud('people_people-performance-cheer1.mp3')
#                read_aloud('shine1.mp3')

        ser.close()

#list=data_refine.execute_in()
#print(list[0])

ser()
#main_path = os.path.dirname(os.path.abspath( __file__ ))
#file_path = os.path.join(main_path, "voices")
#file_path = os.path.join(file_path,"12.うっとりとし.mp3")
#read_aloud(file_path)

#画像を生成する
#def make_png(hist,data):

#画像を印刷する
#def print_png(png):

#ser()
#setup関数
#    print(data)
#列の定義
colnum_same_id = 5
#    print(data["呼応するもの"])
colnum_similar_id = 6
#過去に踏んだもののidを格納する
hist = []

def loop():
    #今踏まれたidを格納
    now_id = 11

#以下繰り返し
#Arduinoから[踏まれたもの、これからひらくもの、...]の配列を受け取る（、これから出す文字列をdfから取り出す）
    book_array = ser()
#    now_id = book_array[0]
    print("now id:",now_id,type(now_id))
    hist.append(now_id)
#Arduinoから読み取った値の音声データを今まで読んでいた音声データの末尾に付け加えて再生する histをread_aloudする的な
#unityに送る文字配列（長さ10）、毎回初期化
    send_u_array = ['']*10
#次に開く位置(Arduinoから送られてきたint列の1番目のセル以降）aをうけとり、Unityに送るchar列a番目に次に使うお文字列の1つをいれる（開かない場所はNaNか0)
#    for i in book_array[1:3]:
#        print(i)
#        print(data["完全一致"][int(now_id)])
    print(data["完全一致"][int(now_id)].split(','))
    print(int(random.sample(data["完全一致"][int(now_id)].split(','),2)[0]))
    print(book_array[1])
    send_u_array[int(book_array[1])] = data["フレーズ"][int(random.sample(data["完全一致"][int(now_id)].split(','),2)[0])]
    send_u_array[int(book_array[2])] = data["フレーズ"][int(random.sample(data["完全一致"][int(now_id)].split(','),2)[1])]
    send_u_array[int(book_array[3])] = data["フレーズ"][int(data["一部一致"][int(now_id)].split(',')[0])]

    print(send_u_array)
    print(','.join(send_u_array))
    return ','.join(send_u_array)

#loop()


#Unityにおくる


#read_aloud("voices/jdee_beat.mp3")

#app = Flask(__name__)
#@app.route("/", methods=['GET'])
def index():
#    return ser()
    return main()
#    return str(send_u_array)
#    return list[ser()[2]]#listの中でser実行結果によって対応する文字列を出す
#    return "あ,い,う,え,お,か,き,く,け,こ"
#
#if __name__ == "__main__":
#    app.debug = True
#    app.run()
