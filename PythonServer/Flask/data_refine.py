#coding:utf-8

import pandas as pd
import csv
import sys
from pykakasi import kakasi

#発音を母音列にかえる(12列め）
def convert_pron(data):
    kakasii = kakasi()
    kakasii.setMode("H","a")
    kakasii.setMode("K","a") # Katakana to ascii, default: no conversion
    kakasii.setMode("J","a") # Japanese to ascii, default: no conversion
    conv = kakasii.getConverter()
    buf=[] #buffer for making new retsu for vowels
    for i in range(len(data)):
        #        print(data[5][i])
        roman = conv.do(data[11][i])#pronounce is in 5 retsume
        #print(roman)
        result=""
        for j in range(len(roman)):
            if roman[j] in vowels:
                result=result+roman[j]
            elif roman[j]=="n":
                if j+1<len(roman):
                    if roman[j+1] not in vowels:
                        result=result+roman[j]
        buf.append(result)
    data[12] = buf
    return data



#data->list of keitaisokaiseki,str->word for search
def search_similar_noun(data,str):
    word_list = []
    for i in range(len(data)):
        flag = 0
        for j in range(1,5):#下から4文字同じやつをさがす
            if ref(data,i,12,j)==str[-j]:
                flag=flag+1
            else:
                break
            
        if flag==4:
            word_list.append(data[3][i-3]+data[3][i-2]+data[3][i-1]+data[3][i])
    return word_list

#文字列の長さによって前の行を参照させる関数 data[retsu][gyo][-i]が存在しないとき
def ref(data,gyo,retsu,i):
    if len(data[retsu][gyo])<i:
        return ref(data,gyo-1,retsu,i-len(data[retsu][gyo]))
    else:
        return data[retsu][gyo][-i]


data = []
vowels =["a","i","u","e","o"]


kumo = pd.read_csv('../../aozora_data/kumonoito.csv',header=None,usecols=[0,1,2,3,4,11])
ginga =pd.read_csv('../../aozora_data/gingatetsudono_yoru.csv',header=None,usecols=[0,1,2,3,4,11])
#print(type(kumo))
print("csv_end")
#実際に実行するもの
def execute_in():
    #print(kumo[11])
    new_kumo = convert_pron(kumo)
    new_ginga = convert_pron(ginga)
    #print(new_kumo)

    #近くなったのでございましょう
    print(search_similar_noun(new_ginga,"ouau"))
    return search_similar_noun(new_ginga,"ouau")
#ローマ字にしてCSVに書き出す
def write_csv(args):
    path = '../../aozora_data/'+args
    data = pd.read_csv(path,header=None,usecols=[0,1,2,3,4,11])
    data = convert_pron(data)
    new_path ='../../aozora_data/new_'+args
    data.to_csv(new_path)
#11列目読み列をつなげてtxtに
def to_yomi_txt(args):
    str = ""
    path = '../../aozora_data/'+args
    data = pd.read_csv(path,header=None,usecols=[11])
    for i in range(len(data)):
        str = str + data[11][i]
    new_path ='../../aozora_data/yomi_txt/new_yomi_'+args.split(".")[0]+".txt"
    file = open(new_path, 'w')  #書き込みモードでオープン
    file.write(str)

#ローマ字母音のみにしてtxtに書き出す
def to_boin_txt(args):
    str= ""
    path = '../../aozora_data/'+args
    data = pd.read_csv(path,header=None,usecols=[11])
    data = convert_pron(data)
    new_path ='../../aozora_data/boin_txt/boin_'+args.split(".")[0]+".txt"
    for i in range(len(data)):
        str = str + data[12][i]
    file = open(new_path, 'w')  #書き込みモードでオープン
    file.write(str)

#ローマ字母音のみにしてcsvに書き出す（原文との対応表)
def to_boin_csv(args):
    path = '../../aozora_data/'+args
    data = pd.read_csv(path,header=None,usecols=[1,3,5,11])
    data = convert_pron(data)
    str_g= ""
    str_y = ""
    str_b = ""
    new_data=pd.DataFrame([["原文"],["読み"],["母音"]])
    j=0
    for i in range(len(data)):
        if i>=1:
            if data[1][i]-data[1][i-1]>=1:
                print("if"+str_g+str_y+str_b)
                new_data = new_data.append(pd.DataFrame([[str_g],[str_y],[str_b]]))
                str_g= ""
                str_y = ""
                str_b = ""
            else:
                str_g = str_g + data[3][i]
                str_y = str_y + data[11][i]
                str_b = str_b + data[12][i]

    new_path ='../../aozora_data/boin_csv/boin_'+args
    print(new_data)
    #    new_data = new_data.T
    new_data.to_csv(new_path)


#print(new_data)
#
#    data = convert_pron(data)
#    new_path ='../../aozora_data/boin_txt/boin_'+args.split(".")[0]+".txt"
#    for i in range(len(data)):
#        str = str + data[12][i]
#    file = open(new_path, 'w')  #書き込みモードでオープン
#    file.write(str)

#execute_in()
#write_csv(sys.argv[1])
#to_yomi_txt(sys.argv[1])
#to_boin_txt(sys.argv[1])
to_boin_csv(sys.argv[1])
