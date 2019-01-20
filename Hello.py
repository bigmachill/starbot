#!/usr/bin/env python
import numpy as np
import io
import cv2

import picamera
from time import sleep

########## PRESS ESCAPE TO EXIT PROGRAM ############

### Outputs/Info
#resolution = (320, 240)
#centered resoltion = (160, 120) -> (0, 0) = resCent
#normal coordinates of the center of the face detection box = (cx, cy) = lorgefacePoint
#centered coordinated of the center of the face detection box = (xCent, yCent) = lorgefaceCeent

with picamera.PiCamera() as camera:
    stream = io.BytesIO()
    camera.resolution = (320, 240)
        


    for foo in camera.capture_continuous(stream, format = 'jpeg'):
        stream.truncate()
        stream.seek(0)
        resCent = (160, 120)
        buff = np.fromstring(stream.getvalue(), dtype = np.uint8)

        img = cv2.imdecode(buff, 1)

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        print "Found " + str(len(faces)) + " face(s)"

        lorgefaceWidth = 0
        lorgefacePoint = (0,0)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cx = x+(w/2)
            cy = y+(h/2)
            print cx, ', ', cy
            xCent = cx - 160
            yCent = cy - 120
            
            if w > lorgefaceWidth:
                lorgefaceWidth = w
                lorgefacePoint = (cx, cy)
                lorgefaceCent = (xCent, yCent)
            print 'lorge boi face: ', lorgefacePoint
                
            
        if lorgefaceWidth == 0:
            print 'stuff goes here ig'
        
        
        cv2.imshow('img', img)
        
        k = cv2.waitKey(1) 
        if k == 27:
            break
            

