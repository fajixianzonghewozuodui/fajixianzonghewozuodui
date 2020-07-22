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
    if len(img_path)>1:
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
            m="\n驾驶人员数量:" + str(driver_num)
            location_info = [['a', 'a', 'a', 'a', 'a'] for k in range(person_num)]
            attribute_info = [['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'] for k in range(person_num)]
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
                    s11=s[0]
                    d11 = d[0]
                    f11 = f[0]
                    g11 = g[0]
                    h11 = h[0]
                    o11 = o[0]
                    k11 = k[0]
                    l11 = l[0]
                    p11 = p[0]
                    s1 ="是"if s11>float(attribute[0])else "否"
                    d1 ="是"if d11> float(attribute[1]) else "否"
                    f1 ="是"if f11 >float( attribute[2]) else "否"
                    g1 ="是"if g11>float(attribute[3])else "否"
                    h1 ="是"if h11>float(attribute[4])else "否"
                    o1 ="是"if o11>float(attribute[5])else "否"
                    k1 ="是"if k11>float(attribute[6])else "否"
                    l1 ="是"if l11>float(attribute[7])else "否"
                    p1 ="是"if p11>float(attribute[8])else "否"

                    attributes = "\n双手离开方向盘:" +"\t分析结果:\t" + s1+ "\t得分:\t" + str(s) + "\t判断值\t" + str(attribute[0]) + \
                                 "\n闭眼:" + "\t"+"\t分析结果:\t" + d1+"\t得分:\t" + str(d)+"\t判断值\t" + str(attribute[1]) + \
                                 "\n未正确佩戴口罩:" +"\t分析结果:\t" + f1+"\t得分:\t" + str(f) + "\t判断值\t" + str(attribute[2]) + \
                                 "\n未系安全带:" + "\t分析结果:\t" + g1+"\t得分:\t" + str(g)+"\t判断值\t" + str(attribute[3])+ \
                                 "\n吸烟:"+"\t"+"\t分析结果:\t" + h1+"\t得分:\t" + str(h) + "\t判断值\t" + str(attribute[4]) + \
                                 "\n使用手机:" + "\t分析结果:\t" + o1+"\t得分:\t" + str(o) + "\t判断值\t" + str(attribute[5]) +  \
                                 "\n视角未看前方:" + "\t分析结果:\t" + k1+"\t得分:\t" + str(k) + "\t判断值\t" + str(attribute[6]) +  \
                                 "\n打哈欠:" +"\t"+ "\t分析结果:\t" + l1+"\t得分:\t" + str(l) + "\t判断值\t" + str(attribute[7]) + \
                                 "\n低头:" + "\t"+"\t分析结果:\t" + p1+"\t得分:\t" + str(p)+ "\t判断值\t" + str(attribute[8])
            f=data+'\n'+attributes
            behavior_message = data+'\n'+attributes
            return behavior_message,img_url
    else:
        str1 = "无图片，请选择一张图片进行识别"
        return str1,"error"
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
        img_path = "i"
        img_url = None
        return filename






if __name__ == '__main__':
    app.run()
