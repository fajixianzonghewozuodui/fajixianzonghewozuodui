import driverBehavior
import plateNumberDefine
import vehicleDetect
import vehicleDamage
import vehicleDefine
from flask import Flask, render_template,request, jsonify


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



#实现了车型识别
@app.route("/selectPicture",methods=["POST"])
def define_open_picture():
    # 通过file标签获取文件
    f = request.files["file"]
    print(f.filename)
    mlist = list(vehicleDefine.open_picture("E:/testimage/test9.jpg"))
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


#实现了车辆检测
@app.route("/selectPictureDetect")
def detect_open_picture():
    mlist = list(vehicleDetect.openPicture())
    i = len(mlist)
    if i == 2:
        return render_template("vehicleDetect.html", picture_url=mlist[1])
    else:
        return render_template("vehicleDetect.html")

@app.route("/defineCarDetect")
def detect_car():
    mlist = list(vehicleDetect.define())
    i = len(mlist)
    print(mlist)
    if i ==2:
        return render_template("vehicleDetect.html",message = mlist[0],picture_url=mlist[1])
    else:
        return render_template("vehicleDetect.html",message = mlist[0])

#实现了车牌识别
@app.route("/selectPictureNumber")
def number_open_picture():
    mlist = list(plateNumberDefine.open_picture())
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
    print(mlist)
    if i ==3:
        return render_template("plateNumberDefine.html",message = mlist[0],picture_url = mlist[1])
    else:
        return render_template("plateNumberDefine.html",message = mlist[0])






#实现了车辆属性识别

#实现了车损识别
@app.route("/selectPictureDamage")
def damage_open_picture():
    mlist = list(vehicleDamage.openPicture())
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

#实现了驾驶行为检测
@app.route("/selectPictureBehavior")
def behavior_open_picture():
    mlist = list(driverBehavior.openPicture())
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

if __name__ == '__main__':
    app.run()