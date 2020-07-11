from flask import Flask,render_template

from aip import AipImageClassify
import tkinter as tk
from tkinter import filedialog
import os
import cv2
import matplotlib.pyplot as plt
import io
import base64

"""
  APPID AK SK
"""
# 在百度云创的实例应用 获取的三个参数填写到下面
APP_ID = '21222085'
API_KEY = 'SMgDfvavkQVr99MlXwgT9hsw'
SECRET_KEY = 'H0AGKvGy04ZCS0dLHGhMA55Yu5f0R2u5'
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
def get_file_content(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

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
    return render_template("vehicleDefine.html")

# 打开图片文件并读取二进制图片信息
@app.route("/defineCar")
def define():
    if len(img_path)>0:
        image = get_file_content(img_path)
        """
          #调用车辆识别的相应API
        """
        # {"top_num": 1} 表示返回的多个车型中的第一个

        # 调用client对象的carDectect方法
        car_message = client.carDetect(image, options={"top_num": 1})["result"][0]["name"]
        return  render_template("vehicleDefine.html",message = car_message,picture_url = img_url)
    else:
        return render_template("vehicleDefine.html",message = "无图片，请选择一张图片进行识别")


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
        return render_template("vehicleDefine.html",picture_url = img_url)
    else:
        return render_template("vehicleDefine.html")






if __name__ == '__main__':
    app.run()
