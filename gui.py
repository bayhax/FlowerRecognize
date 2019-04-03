#!/bin/python
import cv2
import wx
from test import evaluate_one_image
from PIL import Image
import numpy as np
import os


class HelloFrame(wx.Frame):

    def __init__(self,*args,**kw):
        super(HelloFrame,self).__init__(*args,**kw)

        pnl = wx.Panel(self)  #把Panel对象置到框架中，方便其他控件的布局管理

        self.pnl = pnl
        #静态文本，显示这个程序的名称意图
        st = wx.StaticText(pnl, label="花朵识别", pos=(270, 0),style = wx.ST_ELLIPSIZE_MIDDLE)
        
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # 选择图像文件按钮
        btn = wx.Button(pnl, -1, "选择图片", pos = (0,0))
        btn.Bind(wx.EVT_BUTTON, self.OnSelect)#Bind 绑定器，绑定按钮处理的函数事件
        
        #拍摄图片按钮
        btn1 = wx.Button(pnl, -1 , "拍摄照片", pos = (100,0))
        btn1.Bind(wx.EVT_BUTTON,self.OnCamera)

        #底部信息栏
        self.CreateStatusBar()
        self.SetStatusText("花朵识别---baymax")
        
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
        num = 0
        cap = cv2.VideoCapture(0)
        while(1):
            # ret是布尔值，是否采集到图片，frame是截取到的一帧图片
            ret, frame = cap.read()
            # show a frame
            cv2.imshow("camera", frame)
            #&OxFF为了防止出现系统读取ASCII码键之外的值而出现BUG
            if cv2.waitKey(100) & 0xFF == ord('s'):
                savePath = "E:\\python\\FlowerRecognize\\camera\\camera" + str(num) + ".jpg"
                cv2.imwrite(savePath,frame)
                num += 1
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
        sb = wx.StaticBitmap(self.pnl, -1, imageShow.ConvertToBitmap(), pos=(100,80), size=(400,400))
        return sb


if __name__ == '__main__':

    app = wx.App()
    frm = HelloFrame(None, title='花朵识别', size=(600,600))
    frm.Show()  #show方法激活框架输出
    app.MainLoop()