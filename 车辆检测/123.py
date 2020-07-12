import urllib
import base64
import requests

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=RSNlGSHlooTzKtfTdMglk0Sn&client_secret=rsjO33VAia5SrFK0KUEm2DiGL5su4vP0'
response = requests.get(host)
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if content:
    print(type(content))
content_str=str(content, encoding="utf-8")
###eval将字符串转换成字典
content_dir = eval(content_str)
access_token = content_dir['access_token']

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
# 二进制方式打开图片文件
f = open('car1.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())