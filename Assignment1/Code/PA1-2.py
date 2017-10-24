#Jason Hatfield - 29163434
#CSE473 Summer 2017
#PA1 - Question 2

import numpy as np
import cv2
from matplotlib import pyplot as plt 

#Import image
img = cv2.imread('lena_gray.jpg',0)
result = cv2.imread('lena_gray.jpg',0)

#Get image dimensions
rows = img.shape[0]
cols = img.shape[1]

#Initialize plot data
img_hist = np.zeros(256)
cum_hist = np.zeros(256)
tx_fx = np.zeros(256)
result_hist = np.zeros(256)

#Calculate the number of pixels of each intensity
for x in range(0,rows):
    for y in range(0,cols):
        img_hist[img[x][y]] += 1
    
#Summate pixel number of pixels by value to find cumulative histogram    
cum_hist[0] = img_hist[0]
for x in range(1,256):
    cum_hist[x] = cum_hist[x-1] + img_hist[x]
    
#Normalize cumulative data to create lookup table
value = (255.0)/(rows * cols)
for x in range(0, 256):
	tx_fx[x] = round(value * cum_hist[x])
	
#Translate lookup table into result image
for x in range(0,rows-1):
    for y in range(0,cols-1):
        result[x][y] = tx_fx[result[x][y]]
        
#Calculate number of pixels per intensity for result histogram
for x in range(0,rows):
    for y in range(0,cols):
        result_hist[result[x][y]] += 1 
	
#Plot data
plt.figure('Problem 2 - Images and Plots')

#Image histogram
plt.subplot(3,2,1).plot(img_hist)
plt.title('Image Histogram')
plt.xlabel('Intensity')
plt.ylabel('# of Pixels')

#Cumulative Histogram
plt.subplot(3,2,2).plot(cum_hist)
plt.title('Cumulative Histogram')
plt.xlabel('Intensity')
plt.ylabel('# of Pixels')

#Result histogram
plt.subplot(3,2,3).plot(result_hist)
plt.title('Result Histogram)')
plt.xlabel('Intensity')
plt.ylabel('# of Pixels')

#Lookup table
plt.subplot(3,2,4).plot(tx_fx)
plt.title('Transformation Function (Lookup table)')
plt.xlabel('Intensity (img)')
plt.ylabel('Intensity (result)')

#Plot original
plt.subplot(3,2,5).imshow(img, cmap=plt.cm.gray)
plt.xticks([]), plt.yticks([])
plt.title('img')

#Plot result 
plt.subplot(3,2,6).imshow(result, cmap=plt.cm.gray)
plt.xticks([]), plt.yticks([])
plt.title('result')

plt.tight_layout()
plt.show()

#Write enhanced image to disk
cv2.imwrite('enhanced.png',result)
