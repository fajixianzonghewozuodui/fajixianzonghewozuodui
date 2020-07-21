# -*- coding: utf-8 -*-
#!/usr/bin/env python
 
from flask import Flask,render_template

from aip import AipImageClassify
import tkinter as tk
from tkinter import filedialog
import os
import cv2
import matplotlib.pyplot as plt
import io
import base64


#client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id = fUY1iqjYDWveFndRf02PmN3I
client_secret = peydzhociLSdIMG3dM2v0eHSNCymazLy
 
#获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key
#提示用户在本地选择一张汽车图片
def open_picture():
    application_window = tk.Tk()
    application_window.withdraw()  # 将创建的tk窗口隐藏

    # 设置文件对话框会显示的文件类型txt files (*.txt)|*.txt|All files (*.*)|*.*
    my_filetypes = [('all files', '.*'), ('text files', '.txt')]

    # 打开一个文件选择对话框，选择汽车图片,返回选择的文件路径
    filename = filedialog.askopenfilename(parent=application_window,
                                        initialdir=os.getcwd(),
                                        title="请选择一张汽车图片",
                                        filetypes=my_filetypes)
    #用户选择文件后销毁tk窗口
    application_window.destroy()
    if len(filename)>0:
        #获得用户选择的图片存储在服务器上的地址
        global img_url
        img_url = get_img_stream(filename)
        global img_path
        img_path = filename
        return filename,img_url
    else:
        return filename

#车辆属性识别
#filename:图片名（本地存储包括路径）
def vehicle_attr(filename):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_attr"
    
    # 二进制方式打开图片文件
    f = open(filename, 'rb')
    img = base64.b64encode(f.read())
    
    params = dict()
    params['image'] = img
    params['show'] = 'true'
    params = urllib.parse.urlencode(params).encode("utf-8")
    #params = json.dumps(params).encode('utf-8')
    
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        #print(content)
        content=content.decode('utf-8')
        print(content)
        
vehicle_attr('car1.jpg') 


