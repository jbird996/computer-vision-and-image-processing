#Jason Hatfield - 29163434
#CSE473 Summer 2017
#PA1 - Question 1b

import numpy as np
import cv2

#Import image, extract dimensions
img = cv2.imread('lena_gray.jpg',0)
rows = img.shape[0]
cols = img.shape[1]

#Initialize separable Sobel filters
filter1a = np.array([[1],[2],[1]])
filter1b = np.array([[-1,0,1]])
filter2a = np.array([[-1],[0],[1]])
filter2b = np.array([[1,2,1]])

#Initialize resultant matrices
filter1_result = np.zeros((rows,cols))
filter2_result = np.zeros((rows,cols))

#Pad image with a single pixel matching the corresponding pixel on the edge of the image
img = np.pad(img,(1,1),'edge')

#Brute force algorithm for looping the image matrix and applying 1D convolution with vertical array
for x in range(0,rows):
    for y in range(0,cols):
        Gx = (filter1a[0][0] * img[x-1][y]) + (filter1a[1][0] * img[x][y]) + (filter1a[2][0] * img[x+1][y]) 
             
        Gy = (filter2a[0][0] * img[x-1][y]) + (filter2a[1][0] * img[x][y]) + (filter2a[2][0] * img[x+1][y]) 
             
        filter1_result[x][y] = Gx
        filter2_result[x][y] = Gy

#Pad stage 1 image after applying vertical array
filter1_pad = np.pad(filter1_result,(1,1),'edge')
filter2_pad = np.pad(filter2_result,(1,1),'edge')
rows2 = filter2_pad.shape[0]
cols2 = filter2_pad.shape[1]

#Brute force algorithm for looping the image matrix and applying 1D convolution with horizontal array
for x in range(0,rows2-1):
    for y in range(0,cols2-1):
        Gx = (filter1b[0][0] * filter1_pad[x][y-1]) + (filter1b[0][1] * filter1_pad[x][y]) + (filter1b[0][2] * filter1_pad[x][y+1]) 
             
        Gy = (filter2b[0][0] * filter2_pad[x][y-1]) + (filter2b[0][1] * filter2_pad[x][y]) + (filter2b[0][2] * filter2_pad[x][y+1]) 
             
        filter1_result[x-1][y-1] = Gx
        filter2_result[x-1][y-1] = Gy
        
#Write resultant images to disk
cv2.imwrite('Gx_2.png',filter1_result) 
cv2.imwrite('Gy_2.png',filter2_result)

#Code to display imported image
#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
