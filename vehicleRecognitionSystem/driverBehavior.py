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

img_path = None
img_url = None


app = Flask(__name__)





# 打开图片文件并读取二进制图片信息
#实现车辆检测
def define():
    if len(img_path)>0:
        f= get_file_content(img_path)
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=cnRyNINSfxGHNIZuNb1V9cgl&client_secret=UAd7WayZ4aB9GnyWnBPz2UZxi2n4g8lV'
        response = requests.get(host)
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        if content:
            print(type(content))
        content_str = str(content, encoding="utf-8")
        ###eval将字符串转换成字典
        content_dir = eval(content_str)
        access_token = content_dir['access_token']

        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"
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

            #
            person_num = jsonpath.jsonpath(json_temp, '$..person_num')[0]
            # 车载人数
            driver_num = jsonpath.jsonpath(json_temp, '$..driver_num')[0]

            j = 0
            data = ""
            attributes = ""
            while (j < person_num):
                location_info = [['a', 'a', 'a', 'a', 'a'] for k in range(person_num)]
                attribute_info = [['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'] for k in range(person_num)]
                location_info[j][0] = jsonpath.jsonpath(json_temp, '$..score')[j]
                location_info[j][1] = jsonpath.jsonpath(json_temp, '$..top')[j]
                location_info[j][2] = jsonpath.jsonpath(json_temp, '$..left')[j]
                location_info[j][3] = jsonpath.jsonpath(json_temp, '$..width')[j]
                location_info[j][4] = jsonpath.jsonpath(json_temp, '$..height')[j]
                attribute_info[j][0] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 0]
                attribute_info[j][1] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 1]
                attribute_info[j][2] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 2]
                attribute_info[j][3] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 3]
                attribute_info[j][4] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 4]
                attribute_info[j][5] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 5]
                attribute_info[j][6] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 6]
                attribute_info[j][7] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 7]
                attribute_info[j][8] = jsonpath.jsonpath(json_temp, '$..threshold')[j * 9 + 8]
                j = j + 1
                for location in location_info:
                    data = "\n分数:" + str(location[0]) + \
                       "\n距顶部距离:" + str(location[1]) + \
                       "\n距左侧距离:" + str(location[2]) + \
                       "\n宽度:" + str(location[3]) + \
                       "\n高度:" + str(location[4]) + '\n' + data + '\n' + '\n'
                for attribute in attribute_info:
                    attributes = "\nboth_hands_leaving_wheel:" + str(attribute[0]) + \
                             "\neyes_closed:" + str(attribute[1]) + \
                             "\nno_face_mask:" + str(attribute[2]) + \
                             "\nnot_buckling_up:" + str(attribute[3]) + \
                             "\nsmoke:" + str(attribute[4]) + \
                             "\ncellphone:" + str(attribute[5]) + \
                             "\nnot_facing_front:" + str(attribute[6]) + \
                             "\nyawning:" + str(attribute[7]) + \
                             "\nhead_lowered:" + str(attribute[8]) + '\n' + data + '\n' + '\n'
            behavior_message = data+'\n'+attributes
            return behavior_message,img_url
    else:
        str = "无图片，请选择一张图片进行识别"
        return str
"""
            return render_template("driverBehavior.html", message=data+'\n'+attributes, picture_url=img_url)
    else:
        return render_template("driverBehavior.html", message="无图片，请选择一张图片进行识别")
"""

#打开图片
def openPicture():
    application_window = tk.Tk()
    application_window.withdraw()  # 将创建的tk窗口隐藏

    # 设置文件对话框会显示的文件类型txt files (*.txt)|*.txt|All files (*.*)|*.*
    my_filetypes = [('all files', '.*'), ('text files', '.txt')]

    # 打开一个文件选择对话框，选择汽车图片
    filename = filedialog.askopenfilename(parent=application_window,
                                        initialdir=os.getcwd(),
                                        title="请选择一张汽车图片",
                                        filetypes=my_filetypes)
    if len(filename)>0:
        #获得用户选择的图片存储在服务器上的地址
        global img_url
        img_url = get_img_stream(filename)
        global img_path
        img_path = filename
        return filename, img_url
    else:
        return filename






if __name__ == '__main__':
    app.run()