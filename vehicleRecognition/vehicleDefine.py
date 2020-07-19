from flask import Flask,render_template

from aip import AipImageClassify
import tkinter as tk
from tkinter import filedialog
import os
import cv2
import matplotlib.pyplot as plt
import io
import base64
import defineCarColor

"""
author:qiuzhuang
createtime:2020/7/8
updatetime:2020/7/12
"""
# 将在百度云创建的实例应用中的相应的三个参数填写好
APP_ID = '21222085'
API_KEY = 'SMgDfvavkQVr99MlXwgT9hsw'
SECRET_KEY = 'H0AGKvGy04ZCS0dLHGhMA55Yu5f0R2u5'
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
#函数可以根据图片路径获得图片
def get_file_content(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def get_img_stream(img_local_path):
  """
  函数可获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
  img_stream = ''
  with open(img_local_path, 'rb') as img_f:
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream).decode()
  return img_stream

#定义两个全局变量用于获取图片路径以及url
img_path = None
img_url = None


app = Flask(__name__)

"""
@app.route('/')
def hello_world():
    return 'Hello World!'
"""

@app.route("/")
def defin_car():
    return render_template("vehicleDefine.html")

# 对用户选择的图片进行车型识别并将识别结果返回给前端
@app.route("/defineCar")
def define():
    if len(img_path)>0:
        image = get_file_content(img_path)
        #调用相应方法获得汽车的颜色
        car_color = defineCarColor.crop_img(img_path)
        """
          #调用车辆识别的相应API
        """
        # {"top_num": 1} 表示返回的多个车型中的第一个

        # 调用client对象的carDectect方法
        car_message = client.carDetect(image, options={"top_num": 1})["result"][0]["name"]
        return  render_template("vehicleDefine.html",message = car_message,picture_url = img_url,color = car_color)
    else:
        return render_template("vehicleDefine.html",message = "无图片，请选择一张图片进行识别")

#提示用户在本地选择一张汽车图片
@app.route("/selectPicture")
def open_picture():
    application_window = tk.Tk()
    application_window.withdraw()  # 将创建的tk窗口隐藏

    # 设置文件对话框会显示的文件类型txt files (*.txt)|*.txt|All files (*.*)|*.*
    my_filetypes = [('all files', '.*'), ('text files', '.txt')]

    # 打开一个文件选择对话框，选择汽车图片
    filename = filedialog.askopenfilename(parent=application_window,
                                        initialdir=os.getcwd(),
                                        title="请选择一张汽车图片",
                                        filetypes=my_filetypes)
    #用户选择文件后销毁tk窗口
    application_window.destroy()
    print(filename)
    if len(filename)>0:
        #获得用户选择的图片存储在服务器上的地址
        global img_url
        img_url = get_img_stream(filename)
        global img_path
        img_path = filename
        return render_template("vehicleDefine.html",picture_url = img_url)
    else:
        return render_template("vehicleDefine.html")






if __name__ == '__main__':
    app.run()
