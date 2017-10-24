# Jason Hatfield - 29163434
# CSE 473 - PA2 - Question 1.4
# Due: 7/12/17

# View Synthesis

import numpy as np
import cv2

leftImg = cv2.imread('view1.png')
rightImg = cv2.imread('view5.png')
leftDisp = cv2.imread('disp1.png',0)
rightDisp = cv2.imread('disp5.png',0)

rows = leftImg.shape[0]
cols = leftImg.shape[1]

leftImg_gen = np.zeros((rows,cols))
rightImg_gen = np.zeros((rows,cols))

# Left image generation
for x in range(0, rows):
    for y in range(0, cols):
        y_disp = int(leftDisp[x,y] / 2)

        if(y - y_disp < 0):
            y_disp = 0
        else:
            leftImg_gen[x,(y - y_disp),:] = leftImg[x,y,:]
            
# Right image generation
for x in range(0, rows):
    for y in range(0, cols):
        y_disp = int(rightDisp[x,y] / 2)
        
        if(y + y_disp >= rows):
            y_disp = 0
        else:
            rightImg_gen[x,(y + y_disp),:] = rightImg[x,y,:]

# Combining the generated images (fill missing info in left image from right image)
view3_gen = np.copy(leftImg_gen)

for i in range(0, rows):
    for j in range(0, cols):
        if(np.all(leftImg_gen[i,j,:] == np.zeros((1,1), dtype=np.int_))):
            view3_gen[i,j,:] = rightImg_gen[i,j,:]

cv2.imwrite('view3_gen.png', view3_gen)
cv2.imwrite('leftImg_gen.png', leftImg_gen)
cv2.imwrite('rightImg_gen.png', rightImg_gen)