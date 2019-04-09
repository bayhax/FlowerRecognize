# FlowerRecognize
 这是一个图像识别的项目，参考大神的项目，增加了自己的注释，删除了一些不必要的内容，利用大神的CNN模型，增加了opencv利用电脑自带摄像头拍照识别的代码。
 参考的大神的链接https://github.com/bighansome/flower_world
 
## 我使用的各种工具的版本
 win7<br>
 Sypder3.2.3<br>
 python3.6<br>
 opencv4.0.1<br>
 tensorflow1.13.1<br>
 wxpython4.0.4
## 使用方法
 1.先修改文件中训练和checkpoint所要存储的路径，train_dir  和  logs_train_dir<br>
 2.运行train.py文件，这个过程可能要持续几个小时，跟你的电脑配置有关。我的电脑训练了六个小时。电脑渣（生无可恋脸）<br>
 3.运行gui.py程序，两个按钮，选择图片和拍照。可自行选择。
## 2019.4.9更新特别提示
 1.新增的语音识别模块，在gui.py文件，三个全局变量text_num，false_num,right_num是因为我在播放音频时，不知为什么无法关闭，无法重新写入文件，所以每次要保存新的文件名称，故而设置三个全局变量<br>
 2.在text_to_speech等文件中出现的绝对路径写入，复制文件等操作，是因为相对路径有时会出现无法写入打开文件的错误。
