import os
import math
import numpy as np
import tensorflow as tf

#创建存储四种花的图片和标签的列表
roses = []             #玫瑰
label_roses = []
tulips = []            #郁金香
label_tulips = []
dandelion = []         #蒲公英
label_dandelion = []
sunflowers = []        #向日葵
label_sunflowers = []


# 1、获取所有的图片路径名，存放到对应的列表当中，并添加对应的标签序号
#返回训练图片及标签数据，测试图片及标签数据
def get_files(file_dir, ratio):
    for file in os.listdir(file_dir + '/roses'):
        roses.append(file_dir + '/roses' + '/' + file)
        label_roses.append(0)
    for file in os.listdir(file_dir + '/tulips'):
        tulips.append(file_dir + '/tulips' + '/' + file)
        label_tulips.append(1)
    for file in os.listdir(file_dir + '/dandelion'):
        dandelion.append(file_dir + '/dandelion' + '/' + file)
        label_dandelion.append(2)
    for file in os.listdir(file_dir + '/sunflowers'):
        sunflowers.append(file_dir + '/sunflowers' + '/' + file)
        label_sunflowers.append(3)

    # 2、对生成的图片路径和标签List做打乱处理，hstack()按列排序
    image_list = np.hstack((roses, tulips, dandelion, sunflowers))
    label_list = np.hstack((label_roses, label_tulips, label_dandelion, label_sunflowers))

    # 利用shuffle打乱顺序
    temp = np.array([image_list, label_list])
    temp = temp.transpose()
    np.random.shuffle(temp)

    # 将所有的img和label转换成list
    all_image_list = list(temp[:, 0])
    all_label_list = list(temp[:, 1])

    # 将所得List分为两部分，一部分用来训练tra，一部分用来测试val
    # ratio是测试集的比例
    n_sample = len(all_label_list)
    n_val = int(math.ceil(n_sample * ratio))  # 测试样本数  ceil向上取整
    n_train = n_sample - n_val  # 训练样本数

    tra_images = all_image_list[0:n_train]
    tra_labels = all_label_list[0:n_train]
    tra_labels = [int(float(i)) for i in tra_labels]
    val_images = all_image_list[n_train:-1]
    val_labels = all_label_list[n_train:-1]
    val_labels = [int(float(i)) for i in val_labels]

    return tra_images, tra_labels, val_images, val_labels

# 生成训练的batch
# 1、将上面生成的List传入get_batch() ，转换类型，产生一个输入队列queue，因为img和lab
# 是分开的，所以使用tf.train.slice_input_producer()，然后用tf.read_file()从队列中读取图像
#   image_W, image_H, ：设置好固定的图像高度和宽度
#   设置batch_size：每个batch要放多少张图片，一个批次训练多少
#   capacity：一个队列最大多少
def get_batch(image, label, image_W, image_H, batch_size, capacity):
   
    # 数据转换类型
    image = tf.cast(image, tf.string)
    label = tf.cast(label, tf.int32)

    # 构造一个输入队列
    input_queue = tf.train.slice_input_producer([image, label])

    label = input_queue[1]
    image_contents = tf.read_file(input_queue[0])  # 从队列中读取图片

    # 2、将图像解码，不同类型的图像不能混在一起，要么只用jpeg，要么只用png等。
    #由于使用训练和测试的图片数据都是jpg格式，所以用decode_jpeg解码图片，得到像素值
    image = tf.image.decode_jpeg(image_contents, channels=3)

    # 3、数据预处理，对图像进行裁剪、填充、标准化等操作，让计算出的模型更健壮。
    image = tf.image.resize_image_with_crop_or_pad(image, image_W, image_H)
    image = tf.image.per_image_standardization(image)

    # 4、生成batch
    # image_batch: 四维张量 [batch_size, width, height, 3],dtype=tf.float32
    # label_batch: 一维张量 [batch_size], dtype=tf.int32
    image_batch, label_batch = tf.train.batch([image, label],
                                              batch_size=batch_size,
                                              num_threads=32,
                                              capacity=capacity)
    # 重新排列label，行数为[batch_size]，变换成batch_size的列表
    label_batch = tf.reshape(label_batch, [batch_size])
    image_batch = tf.cast(image_batch, tf.float32)
    return image_batch, label_batch