# Jason Hatfield - 29163434
# CSE 473 - PA2 - Question 1.1a
# Due: 7/12/17

# Block Matching 3x3

import cv2
import numpy as np

leftImg = cv2.imread('view1.png', 0)
rightImg = cv2.imread('view5.png', 0)
leftDisp_ground = cv2.imread('disp1.png', 0)
rightDisp_ground = cv2.imread('disp5.png', 0)

# Image Padding
leftImg_padded = cv2.copyMakeBorder(leftImg, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0);
rightImg_padded = cv2.copyMakeBorder(rightImg, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0);

rows = leftImg_padded.shape[0]
cols = leftImg_padded.shape[1]

# Initialize disparity matrices
leftDisp = np.zeros((rows, cols))
rightDisp = np.zeros((rows, cols))

# Calculating Left Disparity - iterate over each row finding minimum ssd, once closest match found, set intensity of disp matrix
for x in range(1, rows - 1):
    for y in range(1, cols - 1):
        block = leftImg_padded[x - 1:x + 2, y - 1:y + 2]
        matchedBlock = 0
        ssd_min = np.iinfo.max
        
        for z in range(y - 100, y):
            if z < 1:
                z = 1
                
            ssd = np.sum(np.square(np.subtract(block, rightImg_padded[x - 1:x + 2, z - 1:z + 2])))

            if ssd < ssd_min:
                ssd_min = ssd
                matchedBlock = z

        leftDisp[x][y] = y - matchedBlock

# Calculating Right Disparity - iterate over each row finding minimum ssd, once closest match found, set intensity of disp matrix

for x in range(1, rows - 1):
    for y in range(1, cols - 1):
        block = rightImg_padded[x - 1:x + 2, y - 1:y + 2]
        matchedBlock = 0
        ssd_min = np.iinfo.max
        
        for z in range(y + 100, y, -1):
            if z >= cols-1:
                z = cols-2
                
            ssd = np.sum(np.square(np.subtract(block, leftImg_padded[x - 1:x + 2, z - 1:z + 2])))

            if ssd < ssd_min:
                ssd_min = ssd
                matchedBlock = z

        rightDisp[x][y] = matchedBlock - y

# Match disparity image size to original image size
leftDisp = leftDisp[1:rows-1, 1:cols-1]
rightDisp = rightDisp[1:rows-1, 1:cols-1]

# Calculate MSE w.r.t ground truth disparity
leftMSE = np.sum(np.square(np.subtract(leftDisp_ground, leftDisp)))
rightMSE = np.sum(np.square(np.subtract(rightDisp_ground, rightDisp)));

leftMSE = leftMSE/(rows*cols)
rightMSE = rightMSE/(rows*cols)

print 'Left MSE (3x3): ', leftMSE
print 'Right MSE (3x3): ', rightMSE

cv2.imwrite("Left_3x3.png",leftDisp)
cv2.imwrite("Right_3x3.png",rightDisp)