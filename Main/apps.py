from django.apps import AppConfig
from igramscraper.instagram import Instagram
# import tensorflow as tf
# import tensorflow_datasets as tfds
import numpy as np
import os
import joblib
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Bots

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

class MainConfig(AppConfig):
    name = 'Main'
    current_path = os.path.dirname(os.path.abspath(__file__))
    instagram = Instagram()

    start = time.time()    
    model1_path = os.path.join(current_path,'model/Sklearn-Models/SVC1.pkl')
    tfidf_path = os.path.join(current_path,'model/Sklearn-Models/tfidf-SVC1.pkl')

    model1 = joblib.load(model1_path)
    tfidf = joblib.load(tfidf_path)

    print("Model and TFIDF loaded in {}s".format(time.time()-start))
    
    # from scheduler import scheduler
    # scheduler.start()

    # def ready(self):
    #     print("Entered Ready")
    #     from scheduler import scheduler
    #     scheduler.start()

# --------------------------------------------------------------------------------------------------------------
# class MultiHeadAttention(tf.keras.layers.Layer):

#   def __init__(self, d_model, num_heads, name="multi_head_attention",**kwargs):
#     super(MultiHeadAttention, self).__init__(name=name,**kwargs)
#     self.num_heads = num_heads
#     self.d_model = d_model
#     assert d_model % self.num_heads == 0

#     self.depth = d_model // self.num_heads

#     self.query_dense = tf.keras.layers.Dense(units=d_model)
#     self.key_dense = tf.keras.layers.Dense(units=d_model)
#     self.value_dense = tf.keras.layers.Dense(units=d_model)

#     self.dense = tf.keras.layers.Dense(units=d_model)

#   def get_config(self):
#       config = super(MultiHeadAttention,self).get_config()
#       config.update({
#           'num_heads':self.num_heads,
#           'd_model':self.d_model,
#       })
#       return config  

#   def attention(self, query, key, value):
#     score = tf.matmul(query, key, transpose_b=True)
#     dim_key = tf.cast(tf.shape(key)[-1], tf.float32)
#     scaled_score = score / tf.math.sqrt(dim_key)
#     weights = tf.nn.softmax(scaled_score, axis=-1)
#     output = tf.matmul(weights, value)
#     return output, weights    

#   def split_heads(self, inputs, batch_size):
#     inputs = tf.keras.layers.Lambda(lambda inputs:tf.reshape(inputs, shape=(batch_size, -1, self.num_heads, self.depth)))(inputs)
#     return tf.keras.layers.Lambda(lambda inputs: tf.transpose(inputs, perm=[0, 2, 1, 3]))(inputs)

#   def call(self, inputs):
#     query, key, value = inputs['query'], inputs['key'], inputs['value']
#     batch_size = tf.shape(query)[0]

#     # linear layers
#     query = self.query_dense(query) # (BS,256)
#     key = self.key_dense(key)
#     value = self.value_dense(value)

#     # split heads
#     query = self.split_heads(query, batch_size) # (BS,-1,8,32) -> (BS,8,-1,32)
#     key = self.split_heads(key, batch_size)
#     value = self.split_heads(value, batch_size)

#     # scaled dot-product attention
#     scaled_attention = self.attention(query, key, value)
#     scaled_attention = scaled_attention[0]

#     scaled_attention = tf.keras.layers.Lambda(lambda scaled_attention: tf.transpose(scaled_attention, perm=[0, 2, 1, 3]))(scaled_attention)
#     # scaled_attention -> (BS,8,-1,32)

#     concat_attention = tf.keras.layers.Lambda(lambda scaled_attention: tf.reshape(scaled_attention,
#                                   (batch_size, -1, self.d_model)))(scaled_attention) # (BS,-1,256)

#     outputs = self.dense(concat_attention)

#     return outputs
