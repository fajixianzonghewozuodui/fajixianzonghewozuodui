import urllib
import base64
import requests
from flask import Flask,render_template

from aip import AipImageClassify
import tkinter as tk
from tkinter import filedialog
import os
import cv2
import matplotlib.pyplot as plt
import io
import base64
import jsonpath
import json
"""
  APPID AK SK
"""

#获取文件内容
def get_file_content(file_path):
    with open(file_path, 'rb') as f:
        return f.read()
#获取文件图片流
def get_img_stream(img_local_path):
  """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
  img_stream = ''
  with open(img_local_path, 'rb') as img_f:
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream).decode()
  return img_stream

img_path = "i"
img_url = None


app = Flask(__name__)


# 打开图片文件并读取二进制图片信息
#实现车辆检测
def define():
    global img_url,img_path
    if len(img_path)>1:
        f= get_file_content(img_path)
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=whRKPIK0qDP5RMtSv1sYhMFo&client_secret=1EuKG9xr5xh7ouB4cZvTLZMVfrAZ4Ggn'
        response = requests.get(host)
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        #if content:
            #print(type(content))
        content_str = str(content, encoding="utf-8")
        ###eval将字符串转换成字典
        content_dir = eval(content_str)
        access_token = content_dir['access_token']

        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_attr"
        # 二进制方式打开图片文件
        f = open(img_path, 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            json_temp = response.json()
            print(json_temp)



            f=json_temp
            img_path = "i"
            return f,img_url
    else:
        str1 = "无图片，请选择一张图片进行识别"
        return str1,"error"

#打开图片
def openPicture(filename):
    if len(filename)>0:
        #获得用户选择的图片存储在服务器上的地址
        global img_url
        img_url = get_img_stream(filename)
        global img_path
        img_path = filename
        return filename, img_url
    else:
        img_path = "i"
        img_url = None
        return filename






if __name__ == '__main__':
    app.run()