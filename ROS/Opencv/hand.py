# -*-coding:utf-8-*-
import cv2
import mediapipe as mp
import time
import math
import cmath
cap = cv2.VideoCapture(0)
#该函数的参数
#static_image_mode,max_num_hands,min_detection_confidence,min_tracking_confidence
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0#开始时间初始化
cTime = 0#目前时间初始化
xs = []
ys = []
ks = []
#大小为21的数组初始化
for i in range(0,21):
    xs.append(0)
    ys.append(0)
for i in range(0,4):
    ks.append(0)
#计算两点间的距离
def point_distance(x1, y1, x2, y2 ):
    dis = abs(math.sqrt((x2 - x1)*(x2 - x1)+(y2 - y1)*(y2 - y1)))
    return dis
def K_count():
    k=5
    i=0
    while(k<20):
        aveX1 = (xs[k] + xs[k+1] + xs[k+2] + xs[k+3]) / 4
        aveY1 = (ys[k] + ys[k+1] + ys[k+2] + ys[k+3]) / 4
        k1 = (xs[k] * ys[k] + xs[k+1] * ys[k+1] + xs[k+2] * ys[k+2] + xs[k+3] * ys[k+3] - 4 * aveX1 * aveY1) / (
                    xs[k] * xs[k] + xs[k+1] * xs[k+1] + xs[k+2] * xs[k+2] + xs[k+3] * xs[k+3] - 4 * aveX1 * aveX1)
        ks[i] = k1
        i += 1
        k += 4
    avek = sum(ks)/4
    ks0 = abs(ks[0] - avek)
    ks1 = abs(ks[1] - avek)
    ks2 = abs(ks[2] - avek)
    ks3 = abs(ks[3] - avek)
    dis = point_distance(xs[12], ys[12], xs[0], ys[0])
    if (ks0+ks1+ks2+ks3) < 3.5 and dis > 100 and abs(ks[1]) > 3:
        print("前进")
    elif (ks0+ks1+ks2+ks3) < 3.5 and dis > 100 and -1 < ks[1] < 0:
        print("左转")
    elif (ks0 + ks1 + ks2 + ks3) < 3.5 and dis > 100 and 0 < ks[1] < 1:
        print("右转")
    elif dis < 100:
        print("停止")
while True:
    count = 0
    success, img = cap.read()#BGR存储格式
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#转为RGB存储
    #处理返回的手的标志点以及处理
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:#返回none或手的标志点坐标
        for handLms in results.multi_hand_landmarks:
            #id是索引，lm是x,y坐标
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
               # print(id, cx, cy)
                xs[id] = cx
                ys[id] = cy
                cv2.circle(img, (cx, cy), 14, (205, 100, 255), cv2.FILLED)
                cv2.putText(img, str(int(id)), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 2,
                (200, 20, 50), 5)
            K_count()
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 1)
    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
        exit()





