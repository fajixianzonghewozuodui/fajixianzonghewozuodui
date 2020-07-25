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
            vehicle_num = jsonpath.jsonpath(json_temp, '$..vehicle_num')
            if vehicle_num==0:
                return "无车辆或图片识别失败",img_url
            i=0
            carm=""
            k=len(vehicle_num)
            while i<k:
                vehicle_type = jsonpath.jsonpath(json_temp, '$..vehicle_type.name')[i]#车辆类型
                vehicle_type_s = jsonpath.jsonpath(json_temp, '$..vehicle_type.score') [i] # 车辆朝向分数
                window_rain_eyebrow = jsonpath.jsonpath(json_temp, '$..window_rain_eyebrow.score')[i] #是否有车窗雨眉
                w ="有"if float(window_rain_eyebrow)>0.02 else "无"
                roof_rack = jsonpath.jsonpath(json_temp, '$..roof_rack.score')[i]#是否有车顶架
                r = "有" if float(roof_rack)>0.01 else "无"
                skylight = jsonpath.jsonpath(json_temp, '$..skylight.score')[i]#是否有天窗
                s = "有" if float(skylight)>0.5 else "无"
                in_car_item= jsonpath.jsonpath(json_temp, '$..in_car_item.score')[i]#是否有车内摆放物
                inf= "有" if float(in_car_item)>0.35 else "无"
                rearview_item = jsonpath.jsonpath(json_temp, '$..rearview_item.score')[i]#是否有后视镜悬挂物
                r1= "有" if 0.4< float(rearview_item) else "无"
                copilot = jsonpath.jsonpath(json_temp, '$..copilot.score')[i]#副驾驶是否有人
                c = "有" if 0.55< float(copilot) else "无"
                driver_belt= jsonpath.jsonpath(json_temp, '$..driver_belt.score')[i]#驾驶位是否系安全带
                d = "有" if 0.75< float(driver_belt) else "无"
                copilot_belt = jsonpath.jsonpath(json_temp, '$..copilot_belt.score') [i] # 副驾驶位是否系安全带
                c1 = "有" if 0.85< float(copilot_belt) else "无"
                driver_visor = jsonpath.jsonpath(json_temp, '$..driver_visor.score') [i] # 驾驶位遮阳板是否放下
                d1 = "有" if 0.2<float(driver_visor) else "无"
                copilot_visor = jsonpath.jsonpath(json_temp, '$..copilot_visor.score') [i] # 副驾驶位遮阳板是否放下
                c2 = "有" if 0.1< float(copilot_visor) else "无"
                direction = jsonpath.jsonpath(json_temp, '$..direction.name')[i]   # 车辆朝向
                direction_s = jsonpath.jsonpath(json_temp, '$..direction.score')[i]  # 车辆朝向分数
                carm=carm+"车辆类型:\t\t"+str(vehicle_type)+"\n识别得分：\t"+str(vehicle_type_s)+'\n'+'\n'\
                "是否有车窗雨眉:\t\t"+w+"\n识别得分：\t"+str(window_rain_eyebrow)+'\n'+'\n'\
                "是否有车顶架:\t\t" +r +"\n识别得分：\t" + str(roof_rack) + '\n'+'\n'\
                "是否有天窗:\t\t" +s +"\n识别得分：\t" + str(skylight) + '\n'+'\n'\
                "是否有车内摆放物:\t" + inf+"\n识别得分：\t" + str(in_car_item) + '\n'+'\n'\
                "是否有后视镜悬挂物:\t" +r1 +"\n识别得分：\t" + str(rearview_item) +'\n'+'\n'\
                "副驾驶是否有人:\t\t" +c +"\n识别得分：\t" + str(copilot) + '\n'+'\n'\
                "驾驶位是否系安全带:\t" + d+"\n识别得分：\t" + str(driver_belt) + '\n'+'\n'\
                "副驾驶位是否系安全带:\t" +c1 +"\n识别得分：\t" + str(copilot_belt) + '\n'+'\n'\
                "驾驶位遮阳板是否放下:\t" + d1+"\n识别得分：\t" + str(driver_visor) + '\n'+'\n'\
                "副驾驶位遮阳板是否放下:\t" + c2+"\n识别得分：\t" + str(copilot_visor) + '\n'+'\n'\
                "车辆朝向:\t\t" +str(direction) +"\n识别得分：\t" + str(direction_s)+'\n'+'\n'
                i=i+1





            m="车辆总数："+str(k)+'\n'+'\n'+carm
            img_path = "i"
            print(m)
            return m,img_url
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