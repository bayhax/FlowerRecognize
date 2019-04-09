# -*- coding: utf-8 -*-
#文字转语音功能
#百度AI平台提供的语音库文件，playsound播放音频
from aip import AipSpeech
from playsound import playsound
import shutil
from real_time_audio import search
#百度AI平台的ID秘钥等，APPID AK SK 
def text2speech(num):
    APP_ID = '15944443'
    API_KEY = 'f9QE5Gd85KeaNOWFG1YGXwvy'
    SECRET_KEY = 'L6wcWCR3ti3sYOOL8IzLALTGenbQsE3L'
    #定义自己的初始化AipSpeech对象
    myspeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    string  = search()
    #print(type(string))
    if len(string) == 0:
        print("请再说一遍：")
        return ""
    else:
        #要转换的文字信息
        result  = myspeech.synthesis("您要寻找的是" + string, 'zh', 1, {
            'spd':5,'pit':9,'vol': 6,'per':4
        })    
        #如果识别正确，则返回语音的二进文件写入自己定义的audio文件中，错误则返回dict
        if not isinstance(result, dict):
            print("写入文件...")
            with open("E:\\python\\Mergetwo\\AudioFile\\audio" + str(num) + ".mp3", 'wb') as f:
                f.write(result)
            print("写入完毕...")
        #测试与gui.pu传过来的计数变量是否一致
        print("text_to_speech: %d" % num)
        #用了绝对路径，因为用相对路径进行文件写入，复制的时候可能会出现无法写入的错误。
        shutil.copy("E:\\python\\Mergetwo\\AudioFile\\audio" + str(num) + ".mp3","E:\\python\\Mergetwo\\AudioCopy\\audio"+str(num)+".mp3")
        playsound("E:\\python\\Mergetwo\\AudioCopy\\audio" + str(num) + '.mp3')
        return string