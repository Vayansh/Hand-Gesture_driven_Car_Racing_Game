import cv2 as cv
import os

vid = cv.VideoCapture(0) 

i = 0
j = 0
k = 0
while True:
    ret, frame = vid.read() 
    if ret == False: break
    
    frame = cv.flip(frame,1)
    cv.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    c = cv.waitKey(1)
    if c%256 == 97:
        cv.imwrite(f'./Dataset/left_hand/{i}.png',frame)
        i+=1
    elif c%256 == 115:
        cv.imwrite(f'./Dataset/right_hand/{j}.png',frame)
        j+=1
    elif c%256 == 100:
        cv.imwrite(f'./Dataset/empty/{k}.png',frame)
        k+=1
    elif c%256 == 113: 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv.destroyAllWindows() 

