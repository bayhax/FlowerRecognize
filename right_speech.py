# -*- coding: utf-8 -*-
#识别正确所播放的语音
from aip import AipSpeech
from playsound import playsound
import shutil

#百度AI平台的ID秘钥等，APPID AK SK """
APP_ID = '15944443'
API_KEY = 'f9QE5Gd85KeaNOWFG1YGXwvy'
SECRET_KEY = 'L6wcWCR3ti3sYOOL8IzLALTGenbQsE3L'
def right(num):
    #定义自己的初始化AipSpeech对象
    myspeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    #要转换的文字信息
    result  = myspeech.synthesis("Bingo,对喽！", 'zh', 1, {
        'spd':5,'pit':9,'vol': 6,'per':4
    })    
    #如果识别正确，则返回语音的二进文件写入自己定义的audio文件中，错误则返回dict
    #以下用的绝对路径，同样是为了避免出现文件写入错误等问题
    if not isinstance(result, dict):
        with open("E:\\python\\Mergetwo\\AudioFile\\right_audio"+str(num)+'.mp3', 'wb') as f:
            f.write(result)
    shutil.copy("E:\\python\\Mergetwo\\AudioFile\\right_audio"+str(num)+'.mp3',"E:\\python\\Mergetwo\\AudioCopy\\right_audio"+str(num)+'.mp3')
    playsound("E:\\python\\Mergetwo\\AudioCopy\\right_audio"+str(num)+'.mp3')
