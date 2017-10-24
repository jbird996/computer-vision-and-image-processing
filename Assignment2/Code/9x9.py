# Jason Hatfield - 29163434
# CSE 473 - PA2 - Question 1.1b
# Due: 7/12/17

# Block Matching 9x9

import cv2
import numpy as np

leftImg = cv2.imread('view1.png', 0)
rightImg = cv2.imread('view5.png', 0)
leftDisp_ground = cv2.imread('disp1.png', 0)
rightDisp_ground = cv2.imread('disp5.png', 0)

# Image Padding
leftImg_padded = cv2.copyMakeBorder(leftImg, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0);
rightImg_padded = cv2.copyMakeBorder(rightImg, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0);

rows = leftImg_padded.shape[0]
cols = leftImg_padded.shape[1]

# Initialize disparity matrices
leftDisp = np.zeros((rows, cols))
rightDisp = np.zeros((rows, cols))

# Calculating Left Disparity - iterate over each row finding minimum ssd, once closest match found, set intensity of disp matrix
for x in range(5, rows - 4):
    for y in range(5, cols - 4):
        block = leftImg_padded[x - 4:x + 5, y - 4:y + 5]
        matchedBlock = 0
        ssd_min = np.iinfo.max
        
        for z in range(y - 100, y):
            if z < 5:
                z = 5
                
            ssd = np.sum(np.square(np.subtract(block, rightImg_padded[x - 4:x + 5, z - 4:z + 5])))

            if ssd < ssd_min:
                ssd_min = ssd
                matchedBlock = z

        leftDisp[x][y] = y - matchedBlock

# Calculating Right Disparity - iterate over each row finding minimum ssd, once closest match found, set intensity of disp matrix

for x in range(5, rows - 4):
    for y in range(5, cols - 4):
        block = rightImg_padded[x - 4:x + 5, y - 4:y + 5]
        matchedBlock = 0
        ssd_min = np.iinfo.max
        
        for z in range(y + 100, y, -1):
            if z >= cols-5:
                z = cols-6
                
            ssd = np.sum(np.square(np.subtract(block, leftImg_padded[x - 4:x + 5, z - 4:z + 5])))

            if ssd < ssd_min:
                ssd_min = ssd
                matchedBlock = z

        rightDisp[x][y] = matchedBlock - y

# Match disparity image size to original image size
leftDisp = leftDisp[4:rows-4, 4:cols-4]
rightDisp = rightDisp[4:rows-4, 4:cols-4]

# Calculate MSE w.r.t ground truth disparity
leftMSE = np.sum(np.square(np.subtract(leftDisp_ground, leftDisp)))
rightMSE = np.sum(np.square(np.subtract(rightDisp_ground, rightDisp)));

leftMSE = leftMSE/(rows*cols)
rightMSE = rightMSE/(rows*cols)

print 'Left MSE (9x9): ', leftMSE
print 'Right MSE (9x9): ', rightMSE

cv2.imwrite("Left_9x9.png",leftDisp)
cv2.imwrite("Right_9x9.png",rightDisp)