# Jason Hatfield - 29163434
# CSE 473 - PA2 - Question 1.2
# Due: 7/12/17

# Block Matching 3x3 with back projection

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
disp_rows = leftDisp_ground.shape[0]
disp_cols = leftDisp_ground.shape[1]

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

# Back projection
leftBP = np.zeros((rows - 2, cols - 2))
rightBP = np.zeros((rows - 2, cols - 2))


for x in range(1, disp_rows):
    for y in range(1, disp_cols):
        leftDisp_val = int(leftDisp[x,y])
        if(y - leftDisp_val >= 1):
            right_val = int(rightDisp[x,(y - leftDisp_val)])
            if(leftDisp_val != right_val):
                leftBP[x,y] = 0
            else:
                leftBP[x,y] = leftDisp[x,y]
                 
        rightDisp_val = int(rightDisp[x,y])
        if(y + rightDisp_val < cols):
            left_val = int(leftDisp[x,(y + rightDisp_val)])
            if(left_val != rightDisp_val):
                rightBP[x,y] = 0
            else:
                rightBP[x,y] = rightDisp[x,y]
                
# Calculate MSE w.r.t ground truth disparity
leftMSE = np.sum(np.square(np.subtract(leftDisp_ground, leftBP)))
rightMSE = np.sum(np.square(np.subtract(rightDisp_ground, rightBP)));

leftMSE = leftMSE/(rows*cols)
rightMSE = rightMSE/(rows*cols)

print 'Left MSE Back Projected (3x3): ', leftMSE
print 'Right MSE Back Projected (3x3): ', rightMSE

cv2.imwrite("Left_3x3_bp.png",leftBP)
cv2.imwrite("Right_3x3_bp.png",rightBP)