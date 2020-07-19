"""
author:qiuzhuang
createtime:2020/7/15
updatetime:2020/7/18
"""
import cv2
import numpy as np
import colorsys
from PIL import Image
import os
from colorsys import rgb_to_hsv

#设定颜色字典
colors = dict((
("红色",(125, 0, 0)),
("橙色",(255, 165, 0)),
("黄色",(255, 255, 0)),
("蓝色",(0, 0, 255) ),
("紫色",(127, 0, 255)),
("黑色",(0, 0, 0)),
("白色",(255, 255, 255)),
("粉色",(255, 192, 203)), ))

# 识别并裁剪出图片中的物体
def crop_img(path):
    # 加载图片，转成灰度图
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 用Sobel算子计算x，y方向上的梯度，之后在x方向上减去y方向上的梯度，通过这个减法，留下具有高水平梯度和低垂直梯度的图像区域。
    gradX = cv2.Sobel(gray, cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, cv2.CV_32F, dx=0, dy=1, ksize=-1)
    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    #去除图像上的噪声，首先使用低通滤泼器平滑图像（9 x 9内核）来平滑图像中的高频噪声。
    # 低通滤波器的目标是降低图像的变化率。如将每个像素替换为该像素周围像素的均值。这样就可以平滑并替代那些强度变化明显的区域。
    # 然后，对模糊图像二值化。梯度图像中不大于90的任何像素都设置为0（黑色）。 否则，像素设置为255（白色）。
    blurred = cv2.blur(gradient, (9, 9))
    _, thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)


    # 用白色填补处理后的图片上的黑色区域
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 分别执行4次形态学腐蚀与膨胀来去掉可能会干扰识别的小斑点
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    # 找出物体区域的轮廓。
    # 使用cv2.findContours()函数
    # 第一个参数是要检索的图片，必须是为二值图，即黑白的（不是灰度图），
    # 所以读取的图像要先转成灰度的，再转成二值图，我们在第三步用cv2.threshold()函数已经得到了二值图。
    # 第二个参数表示轮廓的检索模式，有四种：
    # 1. cv2.RETR_EXTERNAL表示只检测外轮廓
    # 2. cv2.RETR_LIST检测的轮廓不建立等级关系
    # 3. cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
    # 4. cv2.RETR_TREE建立一个等级树结构的轮廓。
    # 第三个参数为轮廓的近似方法
    # cv2.CHAIN_APPROX_NONE存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
    # cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    # cv2.findContours()函数返回两个值，一个是轮廓本身，还有一个是每条轮廓对应的属性。
    # cv2.findContours()函数返回第一个值是list，list中每个元素都是图像中的一个轮廓，用numpy中的ndarray表示。
    # 每一个ndarray里保存的是轮廓上的各个点的坐标。我们把list排序，点最多的那个轮廓就是我们要找的昆虫的轮廓。
    x = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts, _b = x
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    # OpenCV中通过cv2.drawContours在图像上绘制轮廓。
    # 第一个参数是指明在哪幅图像上绘制轮廓
    # 第二个参数是轮廓本身，在Python中是一个list
    # 第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓
    # 第四个参数是轮廓线条的颜色
    # 第五个参数是轮廓线条的粗细
    # cv2.minAreaRect()函数:
    # 主要求得包含点集最小面积的矩形，这个矩形是可以有偏转角度的，可以与图像的边界不平行。

    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

    # 裁剪图片，尽可能多的把除了物体之外的部分去除掉。box里保存的是绿色矩形区域四个顶点的坐标
    # 找出四个顶点的x，y坐标的最大最小值。新图像的高=maxY-minY，宽=maxX-minX。
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    cropImg = image[y1:y1 + hight, x1:x1 + width]

    sp = cropImg.shape  # 获取图像形状：返回【行数值，列数值】列表
    sz1 = sp[0]  # 图像的高度（行 范围）
    sz2 = sp[1]  # 图像的宽度（列 范围）


    # 对图片进一步裁剪，得到车的中间那块部分
    a = int((sz2 * 3) / 5)  # x start
    b = int((sz2 / 20) * 17)  # x end
    c = int((sz1 / 15) * 8)  # y start
    d = int((sz1 * 3) / 5)  # y end
    croImg = cropImg[c:d, a:b]
    cv2.imwrite("croImg.jpg", croImg)

    image = Image.open('croImg.jpg')
    color_to_match = get_dominant_color(image)
    car_color = min_color_diff(color_to_match, colors)
    #返回汽车的颜色
    return car_color

#找出颜色字典中与输入的rgb最接近的颜色，采用求距离的方式，看哪个颜色最接近
def min_color_diff( color_to_match, colors):
    i = 0
    min_distance = 270000
    #保存距离最近的颜色
    max_color = None
    #用循环算出输入的rgb与颜色字典中9种颜色距离最近的颜色
    while(i<len(colors)):
        if i == 0:
            a = (color_to_match[0]-colors["红色"][0])**2+(color_to_match[1]-colors["红色"][1])**2+(color_to_match[2]-colors["红色"][2])**2
            #距离更小就更新max_color变量
            if a<min_distance:
                min_distance = a
                max_color = "红色"
        elif i==1:
            a = (color_to_match[0]-colors["橙色"][0])**2+(color_to_match[1]-colors["橙色"][1])**2+(color_to_match[2]-colors["橙色"][2])**2
            if a<min_distance:
                min_distance = a
                max_color = "橙色"
        elif i==2:
            a = (color_to_match[0]-colors["黄色"][0])**2+(color_to_match[1]-colors["黄色"][1])**2+(color_to_match[2]-colors["黄色"][2])**2
            if a<min_distance:
                min_distance = a
                max_color = "黄色"
        elif i==3:
            a = (color_to_match[0]-colors["蓝色"][0])**2+(color_to_match[1]-colors["蓝色"][1])**2+(color_to_match[2]-colors["蓝色"][2])**2
            if a<min_distance:
                min_distance = a
                max_color = "蓝色"
        elif i==4:
            a = (color_to_match[0]-colors["紫色"][0])**2+(color_to_match[1]-colors["紫色"][1])**2+(color_to_match[2]-colors["紫色"][2])**2
            if a<min_distance:
                min_distance = a
                max_color = "紫色"
        elif i==5:
            a = (color_to_match[0]-colors["黑色"][0])**2+(color_to_match[1]-colors["黑色"][1])**2+(color_to_match[2]-colors["黑色"][2])**2
            if a<min_distance:
                min_distance = a
                max_color = "黑色"
        elif i==6:
            a = (color_to_match[0]-colors["白色"][0])**2+(color_to_match[1]-colors["白色"][1])**2+(color_to_match[2]-colors["白色"][2])**2
            if a<min_distance:
                min_distance = a
                max_color = "白色"
        else:
            a = (color_to_match[0] - colors["粉色"][0]) ** 2 + (color_to_match[1] - colors["粉色"][1]) ** 2 + ( color_to_match[2] - colors["粉色"][2]) ** 2
            if a < min_distance:
                min_distance = a
                max_color = "粉色"
        i = i+1
    #删掉之前存储到本地的图片
    if os.path.exists("croImg.jpg"):
        os.remove("croImg.jpg")
    return max_color



#获得输入的图片中最主要的颜色
def get_dominant_color(image):
    # 要提取的主要颜色数量
    num_colors = 1

    small_image = image.resize((80, 80))
    result = small_image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)  # image with 5 dominating colors

    result = result.convert('RGB')
    # result.show() # 显示图像
    main_colors = result.getcolors(80 * 80)
    return main_colors[0][1]

if __name__ == '__main__':
    crop_img("E:/testimage/test3.jpg")



