import cv2
#read img
img = cv2.imread('ImageTest/image_10.png',1)

print(img)
#show img
cv2.imshow('image',img)