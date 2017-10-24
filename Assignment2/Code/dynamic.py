# Jason Hatfield - 29163434
# CSE 473 - PA2 - Question 1.3
# Due: 7/12/17

# Disparity estimation using dynamic programming

import numpy as np
import cv2

leftImg = cv2.imread("view1.png", 0)
rightImg = cv2.imread("view5.png", 0)
    
rows = leftImg.shape[0]
cols = leftImg.shape[1]
    
# Left / Right Disparity image matrix initialization
leftDisp = np.zeros((rows, cols))
rightDisp = np.zeros((rows, cols))
     
occ = 20
    
# Cost matrix, Direction matrix initialization
cm = np.zeros((cols, cols))
dm = np.zeros((cols, cols))
        
# Populate cost matrix 
for i in range(0, cols):
    cm[i][0] = i * occ
    cm[0][i] = i * occ
    
for r in range (0, rows):
 
    for x in range (0, cols):
        for y in range(0, cols):  
                  
            if(leftImg[r][x] > rightImg[r][y]):
                cost = np.absolute(leftImg[r][x] - rightImg[r][y])           
            else:
                cost = rightImg[r][y] - leftImg[r][x]
 
            min1 = cm[x-1][y-1] + cost
            min2 = cm[x-1][y] + occ
            min3 = cm[x][y-1] + occ
                
            cm[x][y] = min(min1, min2, min3)
            cmin = cm[x][y]
                
            if(min1 == cmin):
                dm[x][y] = 1
            if(min2 == cmin):
                dm[x][y] = 2
            if(min3 == cmin):
                dm[x][y] = 3
        
    x = cols - 1
    y = cols - 1
        
    while (x != 0) and  (y != 0):
        if(dm[x][y] == 1):
            leftDisp[r][x] = np.absolute(x - y)
            rightDisp[r][y] = np.absolute(y - x)
            x = x - 1
            y = y - 1
        elif(dm[x][y] == 2):
            leftDisp[r][x] = 0
            x = x - 1
        elif(dm[x][y] == 3):
            rightDisp[r][y] = 0
            y = y - 1
 
cv2.imwrite("Left_Disp.png",leftDisp)
cv2.imwrite("Right_Disp.png",rightDisp)