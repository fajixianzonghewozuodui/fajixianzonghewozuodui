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
    return render_template("vehicleDetect.html")

# 打开图片文件并读取二进制图片信息
#实现车辆检测
@app.route("/defineCar")
def define():
    if len(img_path)>0:
        f= get_file_content(img_path)
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=RSNlGSHlooTzKtfTdMglk0Sn&client_secret=rsjO33VAia5SrFK0KUEm2DiGL5su4vP0'
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

        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
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
        # 摩托车数量
        motorbike_num = jsonpath.jsonpath(json_temp, '$..motorbike')[0]
        print("摩托车数量", motorbike_num)
        # 三轮车数量
        tricycle_num = jsonpath.jsonpath(json_temp, '$..tricycle')[0]
        print("三轮车数量", tricycle_num)
        # 汽车数量
        car_num = jsonpath.jsonpath(json_temp, '$..car')[0]
        print("汽车数量", car_num)
        # 卡车数量
        truck_num = jsonpath.jsonpath(json_temp, '$..truck')[0]
        print("卡车数量", truck_num)
        # 公交车数量
        bus_num = jsonpath.jsonpath(json_temp, '$..bus')[0]
        print("公交车数量", bus_num)
        # 汽车车牌数量
        carplate_num = jsonpath.jsonpath(json_temp, '$..carplate')[0]
        print("汽车车牌数量", carplate_num)
        # 车辆总数
        vehicle_num = motorbike_num + tricycle_num + car_num + truck_num + bus_num
        print("车辆总数", vehicle_num)
        # 车辆位置
        vehicle_location = [['a', 'a', 'a', 'a', 'a', 'a'] for k in range(vehicle_num + carplate_num)]
        i = 0
        while (i < vehicle_num + carplate_num):
            vehicle_location[i][0] = jsonpath.jsonpath(json_temp, '$..type')[i]
            vehicle_location[i][1] = jsonpath.jsonpath(json_temp, '$..width')[i]
            vehicle_location[i][2] = jsonpath.jsonpath(json_temp, '$..top')[i]
            vehicle_location[i][3] = jsonpath.jsonpath(json_temp, '$..left')[i]
            vehicle_location[i][4] = jsonpath.jsonpath(json_temp, '$..height')[i]
            vehicle_location[i][5] = jsonpath.jsonpath(json_temp, '$..probability')[i]
            i = i + 1
        data=""
        for vehicle in vehicle_location:
            print("车辆类型", vehicle[0])
            print("宽度", vehicle[1])
            print("距顶部距离", vehicle[2])
            print("距左侧距离", vehicle[3])
            print("高度", vehicle[4])
            print("置信度", vehicle[5])
            data="车辆类型:"+str(vehicle[0])+\
                 "\n宽度:"+str(vehicle[1])+\
                 "\n距顶部距离:"+str(vehicle[2])+\
                 "\n距左侧距离:"+str(vehicle[3])+\
                 "\n高度:"+str(vehicle[4])+\
                 "\n置信度:"+str(vehicle[5])+'\n'+data
        car_message="车辆总数："+str(vehicle_num)+\
                    "\n摩托车数量："+str(motorbike_num)+\
                    "\n三轮车数量："+str(tricycle_num)+\
                    "\n汽车数量："+str(car_num)+\
                    "\n卡车数量："+str(truck_num)+\
                    "\n公交车数量："+str(bus_num)+\
                    "\n汽车车牌数量："+str(carplate_num)
        return render_template("vehicleDetect.html",message = car_message+'\n'+data,picture_url = img_url)
    else:
        return render_template("vehicleDetect.html",message = "无图片，请选择一张图片进行识别")

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
        return render_template("vehicleDetect.html",picture_url = img_url)
    else:
        return render_template("vehicleDetect.html")






if __name__ == '__main__':
    app.run()
