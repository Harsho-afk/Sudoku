import cv2
import numpy as np
from Utils import *
import os
import shutil
from keras.utils import load_img
from keras.utils import img_to_array
from keras.models import load_model
import Model

if not os.path.isfile("src/DigitRecognitionModel.keras"):
    Model.createModel()

model = load_model("src/DigitRecognitionModel.keras")
shutil.rmtree("temp/")
os.mkdir("temp/")

image = cv2.imread('src/test.png')
image = cv2.resize(image,(900,900))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(7,7),0)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,57,5)
thresh = cv2.morphologyEx(thresh,cv2.MORPH_DILATE,(7,7))

maxArea = 0
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    area = cv2.contourArea(c)
    if area > 25000:
        peri = cv2.arcLength(c,True)
        polygone = cv2.approxPolyDP(c,0.01*peri,True)
        if area > maxArea and len(polygone) == 4:
            contour_grille = polygone
            maxArea = area

offset = 0
pts1 = np.float32([
                    [contour_grille[0][0][0],contour_grille[0][0][1]],
                    [contour_grille[1][0][0],contour_grille[1][0][1]],
                    [contour_grille[2][0][0],contour_grille[2][0][1]],
                    [contour_grille[3][0][0],contour_grille[3][0][1]],
                   ])
pts2 = np.float32([[0,0],[0,0],[0,0],[0,0]])
for i in range(len(pts1)):
    if pts1[i][0] > 450.0: 
        pts2[i][0] = 900.0
        pts1[i][0] += offset
    else: 
        pts2[i][0] = 0.0
        pts1[i][0] -= offset
    if pts1[i][1] > 450.0: 
        pts2[i][1] = 900.0
        pts1[i][1] += offset 
    else: 
        pts2[i][1] = 0.0
        pts1[i][1] -= offset

matrix = cv2.getPerspectiveTransform(pts1,pts2)
grid = cv2.warpPerspective(image,matrix,(900,900))
grid = cv2.cvtColor(grid,cv2.COLOR_BGR2GRAY)

for i in range(9):
    temp = []
    for j in range(9):
        image = grid[i*100:(i+1)*100,j*100:(j+1)*100]
        cv2.imwrite("temp/"+str(i)+str(j)+".jpg",image)
        
for i in range(9):
    for j in range(9):
        image = cv2.imread("temp/"+str(i)+str(j)+".jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        res,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        cv2.floodFill(thresh,None,(0,0),0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for _, c in enumerate(contours):
            boundRect = cv2.boundingRect(c)
            rectX = boundRect[0]
            rectY = boundRect[1]
            rectWidth = boundRect[2]
            rectHeight = boundRect[3]
            currentCrop = image[rectY-5:rectY+rectHeight+5,rectX-5:rectX+rectWidth+5]
            currentCrop = cv2.resize(currentCrop,(28,28))
            ret, currentCrop = cv2.threshold(currentCrop, 100, 255, cv2.THRESH_BINARY_INV)
            currentCrop = cv2.cvtColor(currentCrop, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("temp/"+str(i)+str(j)+".jpg",currentCrop)

table = np.zeros((9, 9), int)
for i in range(9):
    predictValue = 0
    for j in range(9):
        image = load_img("temp/"+str(i)+str(j)+".jpg", target_size=(28, 28))
        image = img_to_array(image)
        image = image.reshape(1, 28, 28, 1).astype('float32')
        image = image / 255.0
        predictValue = model.predict(image)
        table[i][j] = np.argmax(predictValue)

for i in range(9):
    for j in range(9):
        print(table[i][j],end=' ')
    print()

shutil.rmtree("temp/") 
os.mkdir("temp/")