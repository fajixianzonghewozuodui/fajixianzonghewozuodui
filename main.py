# -*- coding: utf-8 -*-
#!/usr/bin/env python
 
import urllib
import base64
import json
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

