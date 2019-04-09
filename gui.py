#!/bin/python
import cv2
import wx
from test import evaluate_one_image
from text_to_speech import text2speech
from right_speech import right
from false_speech import false
from PIL import Image
import numpy as np
import os

#各个按钮，文本位置的数值，方便日后修改
FRAME_SIZE = (600,600)
IMAGE_SIZE = (400,400)
TEXT_POS = (250,0)
SELECT_POS = (0,0)
CAMERA_POS = (0,30)
AUDIO_POS = (0,60)
#全局变量，为了解决运行过程中无法删除音频文件而设置，保存成不同的文件名播放音频，
#运行完程序后，手动删除，不影响下一次运行
text_num = 0
false_num = 0
right_num = 0
class HelloFrame(wx.Frame):

    def __init__(self,*args,**kw):
        super(HelloFrame,self).__init__(*args,**kw)

        pnl = wx.Panel(self)  #把Panel对象置到框架中，方便其他控件的布局管理

        self.pnl = pnl
        #静态文本，显示这个程序的名称意图
        st = wx.StaticText(pnl, label="花朵识别", pos=TEXT_POS,style = wx.ST_ELLIPSIZE_MIDDLE)
        
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # 选择图像文件按钮
        btn = wx.Button(pnl, -1, "选择图片", pos = SELECT_POS)
        btn.Bind(wx.EVT_BUTTON, self.OnSelect)#Bind 绑定器，绑定按钮处理的函数事件
        
        #拍摄图片按钮
        btn1 = wx.Button(pnl, -1 , "拍摄照片", pos = CAMERA_POS)
        btn1.Bind(wx.EVT_BUTTON,self.OnCamera)
        
        #语音识别图片
        btn2 = wx.Button(pnl,-1,"语音识别", pos = AUDIO_POS)
        btn2.Bind(wx.EVT_BUTTON,self.audio_recognize)

        #底部信息栏
        self.CreateStatusBar()
        self.SetStatusText("花朵识别---baymax")
        
    #语音识别图片
    def audio_recognize(self,event):
        #print(num)
        #使用全局变量，确保每一次运行所需要的语音文件名字不重复。
        #可以删除，就是把你播放的音频文件播放完之后关闭然后删除音频文件，那这些global变量
        #就可以不用设置了，然而我的不知道什么地方出问题了，音频文件没法关闭。
        global text_num
        #测试是第几次识别
        #print("audio_recognize: %d" % text_num)
        string  = text2speech(text_num)
        text_num += 1
        while True:
            if len(string) > 0:
                break
            else:
                print("请再说一遍哦")
                string = text2speech(text_num)
                text_num += 1
        print("你要识别的内容为："+string)
        print("请测试.....")
        self.audio_camera(string)
        
    #语音识别拍照
    def audio_camera(self,string):
        global false_num
        global right_num
        #保存摄像头采集图片所需要的计数变量，防止保存的文件名字重复
        pic_num = 0
        cap = cv2.VideoCapture(0)
        while(1):
            # ret是布尔值，是否采集到图片，frame是截取到的一帧图片
            ret, frame = cap.read()
            # show a frame
            cv2.imshow("camera", frame)
            #&OxFF为了防止出现系统读取ASCII码键之外的值而出现BUG
            if cv2.waitKey(100) & 0xFF == ord('s'):
                savePath = "E:\\python\\Mergetwo\\camera\\camera" + str(pic_num) + ".jpg"
                cv2.imwrite(savePath,frame)
                pic_num += 1
                img = Image.open(savePath)
                imag = img.resize([64, 64])
                image = np.array(imag)
                result = evaluate_one_image(image)
                #如果自己语音说出的种类的名称是识别出的，则显示在界面上，否则不显示，重新录入语音
                if string in result:
                    result_text = wx.StaticText(self.pnl, label=result, pos=(150,40))
                    font = result_text.GetFont()
                    font.PointSize += 8
                    result_text.SetFont(font)
                    self.initimage(name= savePath)
                    right(right_num)
                    right_num += 1
                else:
                    false(false_num)
                    false_num += 1
                    print("不对哦")
                
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
        #释放摄像头资源
        cap.release()
        cv2.destroyAllWindows() 
        
    #读取选择或者拍摄的图片并估计属于哪个类别
    def read_img(self,img):
        imag = img.resize([64, 64])
        image = np.array(imag)
        result = evaluate_one_image(image)
        result_text = wx.StaticText(self.pnl, label=result, pos=(150,40))
        font = result_text.GetFont()
        font.PointSize += 8
        result_text.SetFont(font)
        
    def OnSelect(self, event):
        wildcard = "image source(*.jpg)|*.jpg|" \
                   "Compile Python(*.pyc)|*.pyc|" \
                   "All file(*.*)|*.*"
        dialog = wx.FileDialog(None, "选择图片", os.getcwd(),
                               "", wildcard, wx.ID_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            print(dialog.GetPath())
            img = Image.open(dialog.GetPath())
            self.read_img(img)
            self.initimage(name= dialog.GetPath())
   
    #拍摄照片方法
    def OnCamera(self,event):
        cam_num = 0
        cap = cv2.VideoCapture(0)
        while(1):
            # ret是布尔值，是否采集到图片，frame是截取到的一帧图片
            ret, frame = cap.read()
            # show a frame
            cv2.imshow("camera", frame)
            #&OxFF为了防止出现系统读取ASCII码键之外的值而出现BUG
            if cv2.waitKey(100) & 0xFF == ord('s'):
                savePath = "E:\\python\\Mergetwo\\camera\\camera" + str(cam_num) + ".jpg"
                cv2.imwrite(savePath,frame)
                cam_num += 1
                img = Image.open(savePath)
                self.read_img(img)
                self.initimage(name= savePath)
                
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
        #释放摄像头资源
        cap.release()
        cv2.destroyAllWindows() 

    # 生成图片控件
    def initimage(self, name):
        imageShow = wx.Image(name, wx.BITMAP_TYPE_ANY)#any加载任意格式的图片
        imageShow = imageShow.Scale(200,200)
        sb = wx.StaticBitmap(self.pnl, -1, imageShow.ConvertToBitmap(), pos=(100,80), size=IMAGE_SIZE)
        return sb


if __name__ == '__main__':

    app = wx.App()
    frm = HelloFrame(None, title='花朵识别', size=FRAME_SIZE)
    frm.Show()  #show方法激活框架输出
    app.MainLoop()