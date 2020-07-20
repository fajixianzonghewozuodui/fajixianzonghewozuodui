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

"""
@app.route('/')
def hello_world():
    return 'Hello World!'
"""

@app.route("/")
def definCar():
    return render_template("vehicleDamage.html")

# 打开图片文件并读取二进制图片信息
#实现车辆检测
@app.route("/defineCar")
def define():
    if len(img_path)>0:
        f= get_file_content(img_path)
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=9KS0meTEo6pmtZ6tcxw1CdMN&client_secret=6nAE23Avqe5i1EvpAgo2BhGTifVlYNA9'
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

        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_damage"
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

            numeric_info = jsonpath.jsonpath(json_temp, '$..numeric_info')[0]
            result = jsonpath.jsonpath(json_temp, '$..result')[0]
            f=""
            c=len(result)
            j=0
            data = ""
            while (j< c):
                # 车损位置
                parts = jsonpath.jsonpath(json_temp, '$..parts')[0]
                print("车损位置", parts)
                # 车损类型
                type = jsonpath.jsonpath(json_temp, '$..type')[0]
                print("车损类型", type)
                # 置信度
                probability = jsonpath.jsonpath(json_temp, '$..probability')[0]
                print("置信度", probability)

                j=j+1
                i = 0
                carmessage = "车损位置：" + str(parts) + \
                            "\n车损类型：" + str(type) + \
                            "\n置信度：" + str(probability)
                count = len(numeric_info)
                vehicle_info = [['a', 'a', 'a', 'a', 'a', 'a'] for k in range(count)]
                while (i < count):
                    vehicle_info[i][0] = jsonpath.jsonpath(json_temp, '$..width')[i]
                    vehicle_info[i][1] = jsonpath.jsonpath(json_temp, '$..area')[i]
                    vehicle_info[i][2] = jsonpath.jsonpath(json_temp, '$..ratio')[i]
                    vehicle_info[i][3] = jsonpath.jsonpath(json_temp, '$..height')[i]
                    i = i + 1
                for vehicle in vehicle_info:
                      #print("宽度", vehicle[i][0])
                      #print("面积", vehicle[i][1])
                      #print("角度", vehicle[i][2])
                      #print("高度", vehicle[i][3])
                    data = "\n宽度:" + str(vehicle[0]) + \
                        "\n面积:" + str(vehicle[1]) + \
                        "\n角度:" + str(vehicle[2]) + \
                        "\n高度:" + str(vehicle[3]) + '\n' + data + '\n' + '\n'

                f=f+'\n'+carmessage+'\n'+data
            return render_template("vehicleDamage.html",message = f,picture_url = img_url)
    else:
        return render_template("vehicleDamage.html",message = "无图片，请选择一张图片进行识别")

#打开图片
@app.route("/selectPicture")
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
    print(filename)
    if len(filename)>0:
        #获得用户选择的图片存储在服务器上的地址
        global img_url
        img_url = get_img_stream(filename)
        global img_path
        img_path = filename
        return render_template("vehicleDamage.html",picture_url = img_url)
    else:
        return render_template("vehicleDamage.html")






if __name__ == '__main__':
    app.run()
