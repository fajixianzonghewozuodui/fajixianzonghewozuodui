import driverBehavior
import plateNumberDefine
import vehicleDetect
import vehicleDamage
import vehicleDefine
from flask import Flask, render_template,request, jsonify

import vehiclePropertiesDefine

app = Flask(__name__)

#初始展示界面
@app.route("/")
def initialize_interface():
    return render_template("teamInterface.html")

#展示首页
@app.route("/showProductPage")
def product_page_interface():
    return render_template("productPage.html")

#展示车型识别界面
@app.route("/showDefineCarInterface")
def define_car_interface():
    return render_template("vehicleDefine.html")

#展示车牌识别界面
@app.route("/showPlateNumberInterface")
def define_Number_interface():
    return render_template("plateNumberDefine.html")

#展示车辆检测界面
@app.route("/showDetectCarInterface")
def detect_car_interface():
    return render_template("vehicleDetect.html")

#展示车辆属性识别界面
@app.route("/showDefineCarPropertiesInterface")
def car_properties_interface():
    return render_template("vehiclePropertiesDefine.html")

#展示车损识别界面
@app.route("/showDamageCarInterface")
def damage_car_interface():
    return render_template("vehicleDamage.html")

#展示驾驶行为分析界面
@app.route("/showDriverBehaviorInterface")
def car_behavior_interface():
    return render_template("driverBehavior.html")

#全局变量用于保存要删除的图片文件的路径
img_name_define = "i"
img_name_detect = "i"
img_name_number = "i"
img_name_damage = "i"
img_name_behavior = "i"
img_name_Att = "i"
#实现了车型识别
@app.route("/selectPicture",methods=["POST"])
def define_open_picture():
    # 通过file标签获取文件
    f = request.files["filename"]
    global img_name_define
    path = "img/" + f.filename
    img_name_define = path
    f.save(path)
    mlist = list(vehicleDefine.open_picture(f.filename))
    i = len(mlist)
    if i==2:
        return render_template("vehicleDefine.html",picture_url = mlist[1])
    else:
        return render_template("vehicleDefine.html")


@app.route("/defineCar")
def define_car():
    mlist = list(vehicleDefine.define())
    i = len(mlist)
    if i==3:
        return render_template("vehicleDefine.html",message = mlist[0],color = mlist[1],picture_url = mlist[2])
    else:
        return render_template("vehicleDefine.html",message = mlist[0])
    global img_name_define
    if os.path.exists(img_name_define):
        os.remove(img_name_define)
    #用完一次后将全局变量置为初值，暂时不知道有没有必要，先不加吧
    #img_name_define = "i"


#实现了车辆检测
@app.route("/selectPictureDetect",methods=["POST"])
def detect_open_picture():
    # 通过file标签获取文件
    f = request.files["filename"]
    global img_name_detect
    path = "img/" + f.filename
    img_name_detect = path
    f.save(path)
    mlist = list(vehicleDetect.openPicture(f.filename))
    i = len(mlist)
    if i == 2:
        return render_template("vehicleDetect.html", picture_url=mlist[1])
    else:
        return render_template("vehicleDetect.html")

@app.route("/defineCarDetect")
def detect_car():
    mlist = list(vehicleDetect.define())
    i = len(mlist)
    if i ==2:
        return render_template("vehicleDetect.html",message = mlist[0],picture_url=mlist[1])
    else:
        return render_template("vehicleDetect.html",message = mlist[0])
    global img_name_detect
    if os.path.exists(img_name_detect):
        os.remove(img_name_detect)

#实现了车牌识别
@app.route("/selectPictureNumber",methods=["POST"])
def number_open_picture():
    # 通过file标签获取文件
    f = request.files["filename"]
    global img_name_number
    path = "img/" + f.filename
    img_name_number = path
    f.save(path)
    mlist = list(plateNumberDefine.open_picture(f.filename))
    i = len(mlist)
    if i==2:
        return render_template("plateNumberDefine.html",picture_url = mlist[1])
    else:
        return render_template("plateNumberDefine.html")

@app.route("/defineCarNumber")
def number_define():
    c = plateNumberDefine.CardPredictor()
    c.train_svm()
    mlist = list(c.predict())  # 带检测图片（在test中选择图片，也可以自己添加图片)
    i = len(mlist)
    if i ==3:
        return render_template("plateNumberDefine.html",message = mlist[0],picture_url = mlist[1])
    else:
        return render_template("plateNumberDefine.html",message = mlist[0])
    global img_name_number
    if os.path.exists(img_name_number):
        os.remove(img_name_number)


#实现了车辆属性识别
@app.route("/selectPictureAtt",methods=["POST"])
def Att_open_picture():
    # 通过file标签获取文件
    f = request.files["filename"]
    global img_name_damage
    img_name_damage = f.filename
    f.save(f.filename)
    mlist = list(vehiclePropertiesDefine.openPicture(f.filename))
    i = len(mlist)
    if i == 2:
        return render_template("vehiclePropertiesDefine.html", picture_url=mlist[1])
    else:
        return render_template("vehiclePropertiesDefine.html")

@app.route("/defineCarAtt")
def Att_car():
    mlist = list(vehiclePropertiesDefine.define())
    i = len(mlist)
    if i==2:
        return render_template("vehiclePropertiesDefine.html",message = mlist[0],picture_url=mlist[1])
    else:
        return render_template("vehiclePropertiesDefine.html",message = mlist[0])
    global img_name_Att
    if os.path.exists(img_name_Att):
        os.remove(img_name_Att)





#实现了车损识别
@app.route("/selectPictureDamage",methods=["POST"])
def damage_open_picture():
    # 通过file标签获取文件
    f = request.files["filename"]
    global img_name_damage
    path = "img/" + f.filename
    img_name_damage = path
    f.save(path)
    mlist = list(vehicleDamage.openPicture(f.filename))
    i = len(mlist)
    if i == 2:
        return render_template("vehicleDamage.html", picture_url=mlist[1])
    else:
        return render_template("vehicleDamage.html")

@app.route("/defineCarDamage")
def damage_car():
    mlist = list(vehicleDamage.define())
    i = len(mlist)
    if i==2:
        return render_template("vehicleDamage.html",message = mlist[0],picture_url=mlist[1])
    else:
        return render_template("vehicleDamage.html",message = mlist[0])
    global img_name_damage
    if os.path.exists(img_name_damage):
        os.remove(img_name_damage)

#实现了驾驶行为检测
@app.route("/selectPictureBehavior",methods=["POST"])
def behavior_open_picture():
    # 通过file标签获取文件
    f = request.files["filename"]
    global img_name_behavior
    path = "img/" + f.filename
    img_name_behavior = path
    f.save(path)
    mlist = list(driverBehavior.openPicture(f.filename))
    i = len(mlist)
    if i == 2:
        return render_template("driverBehavior.html", picture_url=mlist[1])
    else:
        return render_template("driverBehavior.html")

@app.route("/defineCarBehavior")
def behavior_define():
    mlist = list(driverBehavior.define())
    i = len(mlist)
    if i==2:
        return render_template("driverBehavior.html",message = mlist[0],picture_url=mlist[1])
    else:
        return render_template("driverBehavior.html",message = mlist[0])
    global img_name_behavior
    if os.path.exists(img_name_behavior):
        os.remove(img_name_behavior)

if __name__ == '__main__':
    app.run()