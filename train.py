import os
import numpy as np
import tensorflow as tf
import input_data
import model

N_CLASSES = 4  # 四种花类型
IMG_W = 64  # resize图像，图片的高和宽，太大的话训练时间久
IMG_H = 64
BATCH_SIZE = 20  #批处理数量
CAPACITY = 200   #容量
MAX_STEP = 10000  # 训练步数，一般大于10K，准确率达到%95以上
learning_rate = 0.0001  # 学习率，不能过大，防止梯度爆炸，也不能过小，训练太慢，一般小于0.0001

# 获取训练批次batch   
train_dir = 'E:\\python\\FlowerRecognize\\input_data'  # 训练样本的读入路径
logs_train_dir = 'E:\\python\\FlowerRecognize\\save'  # logs存储路径，checkpont检查点存储路径

# 从get_files()中获取训练和测试的图片及标签数据列表
train, train_label, val, val_label = input_data.get_files(train_dir, 0.3)
# 每批次训练数据及标签
train_batch, train_label_batch = input_data.get_batch(train, train_label, IMG_W, IMG_H, BATCH_SIZE, CAPACITY)
# 每批次测试数据及标签
val_batch, val_label_batch = input_data.get_batch(val, val_label, IMG_W, IMG_H, BATCH_SIZE, CAPACITY)

# 训练操作定义，logits用于最后做softmax计算的输入
train_logits = model.inference(train_batch, BATCH_SIZE, N_CLASSES)
train_loss = model.losses(train_logits, train_label_batch)
train_op = model.trainning(train_loss, learning_rate)
train_acc = model.evaluation(train_logits, train_label_batch)

# 测试操作定义
test_logits = model.inference(val_batch, BATCH_SIZE, N_CLASSES)
test_loss = model.losses(test_logits, val_label_batch)
test_acc = model.evaluation(test_logits, val_label_batch)

# log汇总记录
summary_op = tf.summary.merge_all()

# 产生一个会话
sess = tf.Session()
# 产生一个writer来写log文件
train_writer = tf.summary.FileWriter(logs_train_dir, sess.graph)
# 产生一个saver来存储训练好的模型
saver = tf.train.Saver()
# 所有节点初始化
sess.run(tf.global_variables_initializer())
# 队列监控,开启线程
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

# 进行batch的训练，'_'只是接受train_op返回的值，并不会在下文使用
try:
    # 执行MAX_STEP步的训练，一步一个batch
    for step in np.arange(MAX_STEP):
        if coord.should_stop():
            break
        _, tra_loss, tra_acc = sess.run([train_op, train_loss, train_acc])

        # 每隔10步打印一次当前的loss以及acc，同时记录log，写入writer
        if step % 10 == 0:
            print('Step %d, train loss = %.2f, train accuracy = %.2f%%' % (step, tra_loss, tra_acc * 100.0))
            summary_str = sess.run(summary_op)
            train_writer.add_summary(summary_str, step)
        # 每隔100步，保存一次训练好的模型
        if (step + 1) == MAX_STEP:
            checkpoint_path = os.path.join(logs_train_dir, 'model.ckpt')
            saver.save(sess, checkpoint_path, global_step=step)

except tf.errors.OutOfRangeError:
    print('Done training -- epoch limit reached')

finally:
    coord.request_stop()    #回收