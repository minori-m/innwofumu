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

send_u_array = ['']*10

#arduinoからのシリアル通信で値を読み取ってstrで返す
def ser():
    with serial.Serial('/dev/cu.usbmodem1411',9600,timeout=1) as ser:
        #int配列の0番目が踏まれたもの、1番目以降が開くもの
        while True:
            print("True loop")
            c = ser.readline().decode('utf8').rstrip()
#            d = re.findall('[0-9]+\.+[0-9]',str(c),flags=0)
#            d = [float(i) for i in d]
#            for i in range(0, len(d)):  #要素を1つずつ順番に出力します
#                print(d[i])
#            print
            print("c=",c)
            if len(c)>0:
                print("c=",c)
                return c
                break

        ser.close()

#list=data_refine.execute_in()
#print(list[0])

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

#画像を生成する
#def make_png(hist,data):

#画像を印刷する
#def print_png(png):

#ser()
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
#対応表
taio = [[1,3,4],[3,4,5],[1,4,5],[4,6,7],[6,7,8],[6,7,8],[4,7,8]]

#はじめの３つのID
hajime = [11,12,13]

def ser_to_unity(ser):
    #今踏まれたidを格納（ここがシリアルで受信したものになる)
    now_id = hajime[ser]
    
#以下繰り返し
#Arduinoから[これからひらくもの、...]の配列を受け取る（、これから出す文字列をdfから取り出す）
    book_array = taio[ser]
#    now_id = book_array[0]
    print("now id:",now_id,type(now_id))
    hist.append(now_id)
#Arduinoから読み取った値の音声データを今まで読んでいた音声データの末尾に付け加えて再生する histをread_aloudする的な
#unityに送る文字配列（長さ10）、毎回初期化
    send_u_array = ['']*9
#次に開く位置(Arduinoから送られてきたint列の1番目のセル以降）aをうけとり、Unityに送るchar列a番目に次に使うお文字列の1つをいれる（開かない場所はNaNか0)
#    for i in book_array[1:3]:
#        print(i)
#        print(data["完全一致"][int(now_id)])
#    print("ichibu=",int(data["一部一致"][int(now_id)].split(',')[0]))
#    print(int(random.sample(data["完全一致"][int(now_id)].split(','),2)[0]))
    print(book_array[1])
    same = data["完全一致"][int(now_id)].split(',')
    similar = data["一部一致"][int(now_id)].split(',')
    same.extend(similar)
    same_del = [i for i in same if i not in hist]
    for i in range(len(book_array)):
        send_u_array[int(book_array[i])] =data["フレーズ"][int(random.sample(same,3)[i])]
#        if random.choice(same) not in hist:
#            print("fraise=",data["フレーズ"][2],int(random.choice(same))
#            send_u_array[int(book_array[i])] = data["フレーズ"][random.choice(same)]
#
    print(send_u_array)
#    print(','.join(send_u_array))
    return ','.join(send_u_array)

ser_to_unity(1)


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

#if __name__ == "__main__":
#    app.debug = True
#    app.run()
