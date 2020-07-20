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
    return render_template("driverBehavior.html")

# 打开图片文件并读取二进制图片信息
#实现车辆检测
@app.route("/defineCar")
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
            f=""
            location_info = [['a', 'a', 'a', 'a', 'a'] for k in range(person_num)]
            attribute_info = [['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'] for k in range(person_num)]
            s = [['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'] for k in range(person_num)]
            while (j < person_num):

                location_info[j][0] = jsonpath.jsonpath(json_temp, '$..location.score')[j]
                location_info[j][1] = jsonpath.jsonpath(json_temp, '$..top')[j]
                location_info[j][2] = jsonpath.jsonpath(json_temp, '$..left')[j]
                location_info[j][3] = jsonpath.jsonpath(json_temp, '$..width')[j]
                location_info[j][4] = jsonpath.jsonpath(json_temp, '$..height')[j]
                s= jsonpath.jsonpath(json_temp, '$..attributes.both_hands_leaving_wheel.score')
                d= jsonpath.jsonpath(json_temp, '$..attributes.eyes_closed.score')
                f= jsonpath.jsonpath(json_temp, '$..attributes.no_face_mask.score')
                g= jsonpath.jsonpath(json_temp, '$..attributes.not_buckling_up.score')
                h= jsonpath.jsonpath(json_temp, '$..attributes.smoke.score')
                o= jsonpath.jsonpath(json_temp, '$..attributes.cellphone.score')
                k= jsonpath.jsonpath(json_temp, '$..attributes.not_facing_front.score')
                l= jsonpath.jsonpath(json_temp, '$..attributes.yawning.score')
                p= jsonpath.jsonpath(json_temp, '$..attributes.head_lowered.score')
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
                       "\n高度:" + str(location[4]) + '\n'
                for attribute in attribute_info:
                   attributes = "\n双手离开方向盘:" +"\t判断值"+str(attribute[0]) +"\t得分：" +str(s)+\
                             "\n闭眼:" + "\t判断值"+str(attribute[1]) + "\t得分：" +str(d)+\
                             "\n未正确佩戴口罩:" + "\t判断值"+str(attribute[2]) + "\t得分：" +str(f)+\
                             "\n未系安全带:" + "\t判断值"+str(attribute[3]) + "\t得分："+str(g)+\
                             "\n吸烟:" + "\t判断值"+str(attribute[4]) + "\t得分："+str(h)+\
                             "\n使用手机:" +"\t判断值"+ str(attribute[5]) + "\t得分：" +str(o)+\
                             "\n视角未看前方:" + "\t判断值"+str(attribute[6]) + "\t得分：" +str(k)+\
                             "\n打哈欠:" +"\t判断值"+ str(attribute[7]) + "\t得分：" +str(l)+\
                             "\n低头:" + "\t判断值"+str(attribute[8]) +"\t得分："+str(p)
            f=data+'\n'+attributes
        return render_template("driverBehavior.html", message=f, picture_url=img_url)
    else:
        return render_template("driverBehavior.html", message="无图片，请选择一张图片进行识别")


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
        return render_template("driverBehavior.html",picture_url = img_url)
    else:
        return render_template("driverBehavior.html")






if __name__ == '__main__':
    app.run()
