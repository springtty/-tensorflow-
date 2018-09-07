#
# Author: Philipp Jaehrling philipp.jaehrling@gmail.com)
#
from collections import OrderedDict

import numpy as np
import tensorflow as tf

from my_models.model import Model
from preprocessing import resize_crop_new
from weight_loading.numpyfile import load_weights
from helper.layer import fc, conv


class VGG(Model):
    """
    VGG16 model definition for Tensorflow
    """
    image_size = 672
    image_prep = resize_crop_new

    def __init__(self, tensor, keep_prob=1.0, num_classes=1000, retrain_layer=['fc6','fc7','fc8'], weights_path='../weights/vgg16.npy'):
        # Call the parent class, which will create the graph
        Model.__init__(self, tensor, keep_prob, num_classes, retrain_layer, weights_path)

        # Call the create function to build the computational graph
        self.final, self.endpoints = self.create()

    def get_final_op(self):
        return self.final

    def get_endpoints(self):
        return self.endpoints

    def get_restore_vars(self):
        return [v for v in tf.global_variables() if not v.name.split('/')[0] in self.retrain_layer]

    def get_retrain_vars(self):
        return tf.trainable_variables()

    def load_initial_weights(self, session):
        load_weights(session, self.weights_path, self.retrain_layer)

    def create(self):
        # 1st Layer: Conv -> Conv -> Pool
        # conv(tensor, filter_height, filter_width, num_filters, stride_y, stride_x, name, padding)
        conv1_1 = conv(self.tensor, 3, 3, 64, 1, 1, padding='SAME', name='conv1_1',
                       trainable=self.is_layer_trainable('conv1_1'))
        conv1_2 = conv(conv1_1, 3, 3, 64, 1, 1, padding='SAME', name='conv1_2',
                       trainable=self.is_layer_trainable('conv1_2'))
        pool1 = tf.nn.max_pool(conv1_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool1')

        # 2nd Layer: Conv -> Conv -> Pool
        conv2_1 = conv(pool1, 3, 3, 128, 1, 1, padding='SAME', name='conv2_1',
                       trainable=self.is_layer_trainable('conv2_1'))
        conv2_2 = conv(conv2_1, 3, 3, 128, 1, 1, padding='SAME', name='conv2_2',
                       trainable=self.is_layer_trainable('conv2_2'))
        pool2 = tf.nn.max_pool(conv2_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool2')

        # 3rd Layer: Conv -> Conv -> Conv -> Pool
        conv3_1 = conv(pool2, 3, 3, 256, 1, 1, padding='SAME', name='conv3_1',
                       trainable=self.is_layer_trainable('conv3_1'))
        conv3_2 = conv(conv3_1, 3, 3, 256, 1, 1, padding='SAME', name='conv3_2',
                       trainable=self.is_layer_trainable('conv3_2'))
        conv3_3 = conv(conv3_2, 3, 3, 256, 1, 1, padding='SAME', name='conv3_3',
                       trainable=self.is_layer_trainable('conv3_3'))
        pool3 = tf.nn.max_pool(conv3_3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool3')

        # 4th Layer: Conv -> Conv -> Conv -> Pool
        conv4_1 = conv(pool3, 3, 3, 512, 1, 1, padding='SAME', name='conv4_1',
                       trainable=self.is_layer_trainable('conv4_1'))
        conv4_2 = conv(conv4_1, 3, 3, 512, 1, 1, padding='SAME', name='conv4_2',
                       trainable=self.is_layer_trainable('conv4_2'))
        conv4_3 = conv(conv4_2, 3, 3, 512, 1, 1, padding='SAME', name='conv4_3',
                       trainable=self.is_layer_trainable('conv4_3'))
        pool4 = tf.nn.max_pool(conv4_3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool4')

        # 5th Layer: Conv -> Conv -> Conv -> Pool
        conv5_1 = conv(pool4, 3, 3, 512, 1, 1, padding='SAME', name='conv5_1',
                       trainable=self.is_layer_trainable('conv5_1'))
        conv5_2 = conv(conv5_1, 3, 3, 512, 1, 1, padding='SAME', name='conv5_2',
                       trainable=self.is_layer_trainable('conv5_2'))
        conv5_3 = conv(conv5_2, 3, 3, 512, 1, 1, padding='SAME', name='conv5_3',
                       trainable=self.is_layer_trainable('conv5_3'))
        pool5 = tf.nn.max_pool(conv5_3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool5')

        # 6th Layer: FC -> DropOut
        # [1:] cuts away the first element
        # pool5_out = int(np.prod(pool5.get_shape()[1:]))  # 7 * 7 * 512 = 25088
        # pool5_flat = tf.reshape(pool5, [-1, pool5_out])  # shape=(image count, 7, 7, 512) -> shape=(image count, 25088)
        # fc6 = fc(pool5_flat, num_out=4096, name='fc6', relu=True, trainable=self.is_layer_trainable('fc6'))
        # dropout1 = tf.nn.dropout(fc6, self.keep_prob)
        #
        # # 7th Layer: FC
        # fc7 = fc(dropout1, num_out=4096, name='fc7', relu=True, trainable=self.is_layer_trainable('fc7'))
        # dropout2 = tf.nn.dropout(fc7, self.keep_prob)
        #
        # # 8th Layer: FC
        # fc8 = fc(dropout2, num_out=self.num_classes, name='fc8', relu=False, trainable=self.is_layer_trainable('fc8'))

        # add layers to the endpoints dict
        endpoints = OrderedDict()
        endpoints['conv1/conv1_1'] = conv1_1
        endpoints['conv1/conv1_2'] = conv1_2
        endpoints['pool1'] = pool1
        endpoints['conv2/conv2_1'] = conv2_1
        endpoints['conv2/conv2_2'] = conv2_2
        endpoints['pool2'] = pool2
        endpoints['conv3/conv3_1'] = conv3_1
        endpoints['conv3/conv3_2'] = conv3_2
        endpoints['conv3/conv3_3'] = conv3_3
        endpoints['pool3'] = pool3
        endpoints['conv4/conv4_1'] = conv4_1
        endpoints['conv4/conv4_2'] = conv4_2
        endpoints['conv4/conv4_3'] = conv4_3
        endpoints['pool4'] = pool4
        endpoints['conv5/conv5_1'] = conv5_1
        endpoints['conv5/conv5_2'] = conv5_2
        endpoints['conv5/conv5_3'] = conv5_3
        endpoints['pool5'] = pool5
        #endpoints['pool5/flat'] = pool5_flat  # 25088
        # endpoints['fc6'] = fc6  # 4096
        # endpoints['fc7'] = fc7  # 4096
        # endpoints['fc8'] = fc8  # number of output classes

        return pool5, endpoints
