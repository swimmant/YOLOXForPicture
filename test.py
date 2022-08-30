import cv2
img = cv2.imread("noshot.jpg")


import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(1):
    # get a frame
    ret, frame = cap.read()
    img=frame

    # 图像切分的尺寸 (3*3)可以自己设置
    cut_size = 3
    # 灰度图
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 拉普拉斯变换
    gray_lap = cv2.Laplacian(grey_img, cv2.CV_64F)

    grey_img_shape = grey_img.shape
    height, width = grey_img_shape[0], grey_img_shape[1]
    height_div = height // cut_size
    width_div = width // cut_size

    # 循环的尺寸，这样循环就不会取到边界
    range_height_size = height_div * cut_size
    range_width_size = width_div * cut_size


    # 切分循环
    cap_count = 0
    no_cap_count = 0
    for i in range(0, range_height_size, height_div):
        for j in range(0, range_width_size, width_div):
            # 获取当前区域的灰度图像素
            subimg = grey_img[j: j+width_div, i: i+height_div]
            # 获取当前区域 拉普拉斯算子 的边缘信息像素信息
            sublap = gray_lap[j: j+width_div, i: i+height_div]

            # 获取标准差
            stddev_g = np.std(subimg)
            stddev_l = np.std(sublap)
            if stddev_g < 25 and stddev_l < 10:
                cap_count+=1
            else:
                no_cap_count += 1
    if no_cap_count>cap_count:
        print('no')
    else:
        print('yes')
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 
