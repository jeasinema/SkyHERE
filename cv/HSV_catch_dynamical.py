# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
color = [0, 0]
flag = True
flag1 = True
count = 0

#TODO:
#1.提高速度，目前增加抓取后速度太慢
#2.矫正畸变
#(1)显示图片：频率约为10Hz
#(2)增加矫正，不显示图片：频率约为14Hz
#(3)不作任何处理：频率约为16Hz
#3.改至HSV色系处理
mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
def select_point(event,x,y,flags,param): 
    #local variable as default, so we should add the global tag
    global flag
    global color 
    global frame
    color = [x,y]
    if (event == cv2.EVENT_LBUTTONDOWN) and (flag):
        print color
        # 图片坐标是反的, 但是作图则是正的！
        cv2.circle(frame, (x, y), 10, (255, 0, 0), 0)
        frame = cv2.undistort(frame, mtx, dist)
        cv2.imshow('image', frame)
        print frame[y,x,:]
        flag = False
        print "click"
        cv2.waitKey(0)

cv2.namedWindow('image') 
cv2.setMouseCallback('image',select_point)
#mouse to select the target
while(flag):
    try:
        ret, frame = cap.read()
        if ret != 1:
            raise IOError
        #创建图像与窗口并将窗口与回调函数绑定 
        frame = cv2.undistort(frame, mtx, dist)
        cv2.imshow('image', frame)
        cv2.waitKey(1)
    except IOError:
        continue
#recognize the color
green = frame[color[1], color[0], :]
#green = [42,144,78]
print green
#cv2.waitKey(0)
threshold = 42 
c = np.zeros((48, 64, 3), np.float32)
mask = np.zeros((60, 80), np.uint8)
while(True):
    try:
        ret, a = cap.read()
        if ret != 1:
            raise IOError
    except IOError:
        continue
    a = cv2.undistort(a, mtx, dist)

    #作图时坐标是正的
    cv2.circle(a, (color[0], color[1]), 10, (255, 0, 0), 0)
    a_hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
    #取点时坐标是反的
    cv2.putText(a,'HSV' + (str)(color) + (str)(a_hsv[color[1], color[0], :]),(color[0], color[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(255, 0, 0))
    print 'HSV', color, a_hsv[color[1], color[0], :]

    #a = cv2.imread('mvtest2.png')
    #cv2.imshow('test', a)
    #cv2.waitKey(-1)
    #for i in range(1, 3):
    #Attention! cannot use numpy.resize!!
    
  
    #TODO:
    #采用高斯模糊后掩膜出现带状干扰图形,检查下原因
    #不能用较大的高斯核对小尺寸图片进行处理
    a = cv2.GaussianBlur(a, (5, 5), 0, 0)
    

    # 转换到 HSV 
    c = cv2.resize(a, (80,60))
    c = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    
  

    # 设定颜色的阈值(Method1: HSV空间的绿色，与选择区域无关) 
    lower_green = np.array([40, 65, 65])   #滤除暗色区域,应用场景环境光比较亮
    upper_green = np.array([80, 256, 256])  #实测发现明度取256时该点仍能分辨颜色
    #实验结果:
    #       1.亮度较大的区域（V值较大）表现为色调上升，从而导致掩膜构建失效，建议初步利用V值动态调节H的阈值
    #       2.SVM？
    #       3.先做模糊处理,然后动态阈值

    #TODO:
    #测试结果20160224：
    # 动态阈值下，强光中心位置可以实现较好的辨识颜色，而此时静态阈值已经无法正常辨识色彩
    #下一步工作：1. 改进动态阈值拟合函数 2. 降噪，降低杂色区域噪声(如毛衣等)   3.补充动态插值法
    #Method2: 根据鼠标点选的区域选择颜色

    # 根据动态阈值构建掩膜
        
    mask_static = cv2.inRange(c, lower_green, upper_green)
    

    #线性模型中的阈值中间量建议通过全局光评价获得
    #实测表明，全局评测下，局部区域受影响较小


    #再次分析明度对色调的影响：
    #TODO：明确需要解决的问题-》强光源附近tag的识别
#                -》根据明度设置动态阈值
#                -》根据全局颜色明度评价设置动态阈值的基值
#                -》
#    当明度增大到一定程度后，对色调的提升作用并不明显
#    同时发现暗区对于色调的影响不大
#    进一步测试发现，静态阈值的鲁棒性好于预期
#    再进一步测试:发现在正确使用动态阈值后（仅处理正向色调偏移，合理设置最大阈值，捕捉明度极大的点）动态阈值还是有一些效果的
#    建议转为进行中心查找算法的优化，试试findcounter
    
    #全局光评价
    amount = 0  
    for i in range(1, 60):
        for j in range(1, 80):
            amount = amount + c[i ,j, 2]
    amount = amount / (60 * 80)
    #print amount



    for i in range(1, 60):
        for j in range(1, 80):
            h_delta = np.float32(c[i, j, 2] - amount) / 100  * 60
           #最大范围建议通过直接采样获得
            if h_delta > 40: 
                h_delta = 40
            if h_delta < -40:
                h_delta = -40
            if h_delta  > 0:    #仅处理强光侧的色调偏移
                low_val = 50    #下阈值不处理
                up_val = 70 + h_delta
            else:
                low_val = 40
                up_val = 80

            #print low_val, c[i,j,0], c[i,j,2], up_val
            #cv2.waitKey(0)
            if (low_val < c[i, j, 0] < up_val) and (lower_green[1] < c[i, j, 1] < upper_green[1]) and (lower_green[2] < c[i, j, 2] < upper_green[2]):
                #图像矩阵255才是最亮！
                mask[i, j] = 255
            else:
                mask[i, j] = 0



    #print mask_static.shape, mask.shape
    #print mask_static.dtype, mask.dtype
    
    #cv2.waitKey(0)

    #mask = cv2.inRange(c, lower_green , upper_green)
    #c = np.float32(c)
    ## 对原图像和掩模进行位运算 
    #res = cv2.bitwise_and(a, a, mask=mask)
    
    #TODO:使用Canny边缘检测和连通域查找进一步滤波，寻找最大连通域
    #发现问题：1. static的mask在边缘抓取时出现了无法识别的问题
    #          2. 强光背景下鲁棒性较好,但是出现了其他连通域的干扰，事实上，高处飞过时仅仅使用连通域大小的判据看来不一定能把色块抠出来
    #             事实上，求连通域再进一步求解中心点的坐标与直接对二值图形求解重心的区别在于findcounter可以找出所有的连通域（返回list）然后可以根据大小再次求解


    #二值图像的降噪处理：开运算，目的为减少噪声连通域的产生
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    #mask_1 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    mask_static = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    #mask_static = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    #TODO:20160225
    #findcontours有时候会存在不能找到目标连通域的问题

    edge_canny_dynamic = cv2.Canny(mask, 100, 200, apertureSize = 7)
    edge_canny_static = cv2.Canny(mask_static, 100, 200, apertureSize = 7)
    
    edge_canny_dynamic = cv2.dilate(edge_canny_dynamic, (3, 3))
    edge_canny_static = cv2.dilate(edge_canny_static, (3, 3))
   
   #TODO: 20160226
   #原因：canny适用于检测剧烈变化的特定边缘的边缘检测，对于此应用场景而言，直接findcontours比较好 
    cot_static = cv2.findContours(mask_static, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    cot_dynamic = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
    print len(cot_static) 
#    cv2.imshow('a', edge_canny_dynamic)
#    cv2.waitKey(1)
#
#    print len(cot_dynamic)
#    print "+++"
#    cv2.waitKey(0)
#    #排序寻找最大区域
    area_dynamic = area_static = []
    for i in cot_static:
        area_dynamic.append(cv2.contourArea(i))
#    area_static.append(i for i in [cv2.contourArea(j)] for j in cot_static)

#
    sort = area_dynamic
    sort.sort()
    #reverse 本身不做排序
    sort.reverse()
    bakg = np.zeros((60,80), np.uint8)
    bakg1 = np.zeros((60,80), np.uint8)
    if len(area_dynamic) > 0:
        cv2.drawContours(bakg, cot_static, area_static.index(sort[0]), (255, 0, 0), 1)
        cv2.drawContours(bakg1, cot_static, -1, (255, 0, 0), 3)
    cv2.imshow('board', bakg)
    cv2.imshow('board_all', bakg1)
    #20160225存在问题：
    # 最大连通域存在频繁跳动，最大连通域被多个小区域分割:原因就是dynamic的mask存在严重的不连续问题
    # 动态阈值的中间空洞问题
    # 考虑对二值图像进行降噪处理？

#    for i in range(0, len(cot_dynamic)-1):
#        print i
#        cv2.drawContours(c, cot_dynamic, 1, (255, 0, 0), 3)
#        cv2.imshow('board', c)
#        cv2.imshow('edge', edge_canny_dynamic)
#        cv2.waitKey(0)
##

    ret = cv2.moments(mask)
    if ret['m00'] != 0:
        x= (int)((float)(ret['m10'])/(float)(ret['m00']))
        y= (int)((float)(ret['m01'])/(float)(ret['m00']))
    else:
        x = y = 0
    
    #print  time.clock(), a_hsv[color[1], color[1], :]
    if flag1:    
        if x < 624 and y < 464:
            cv2.circle(a, ((int)(x*8), (int)(y*8)), 50, (255, 0, 0), 0)
        cv2.imshow('mask_dynamic_edge', edge_canny_dynamic)
        cv2.waitKey(1)
        cv2.imshow('mask_static_edge', edge_canny_static)
        cv2.waitKey(1)
        cv2.imshow('image', a_hsv)
        cv2.waitKey(1)
        cv2.imshow('image_a', a)
        cv2.waitKey(1)
        cv2.imshow('mask_dynamic', mask)
        cv2.waitKey(1)
        cv2.imshow('mask_static', mask_static)
        cv2.waitKey(1)
        #cv2.imshow('mask_dynamic_new', mask_1)
        #cv2.waitKey(1)
    #print time.clock()
    if cv2.waitKey(10) & 0xFF == ord('o'):
        flag1 = False
        print "+++++++++"
        cv2.destroyWindow('image')
    #if flag1:
    #   cv2.imwrite('./saved2/'+(str)(count)+'.png', a) 
    #   count = count + 1
    #   print time.clock()
