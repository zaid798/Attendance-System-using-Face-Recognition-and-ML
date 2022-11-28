import datetime

import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import mysql.connector
import time
mysql = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd ="987123456Z@id",
    database = "project_attendance"
)
path = "ImageAttendance"

images = []
className = []
myList = os.listdir(path)
print(myList)
for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    className.append(os.path.splitext(cls)[0])
print(className)
def findencodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListknown =  findencodings(images)
print("encoding complete")
def attendance(name,count):
    if count<=9:
        with open("Attendance.csv","r+") as f:
            myDataList =f.readlines()
            d = {}
            for line in myDataList:
                entry = line.split(",")
                d[entry[0]]=0
            if name not in d:
                time_now = datetime.now()
                tstr = time_now.strftime("%H:%M:%S")
                f.writelines(f"\n{name},{tstr}")
                mycusror=mysql.cursor()
                sql="insert into new_table(name,time) value(%s,%s)"
                val = [(name),(tstr)]
                mycusror.execute(sql,val)
                mysql.commit();
                print("data is saved")
    else:
        f = open("Attendance.csv", "w")
        f.truncate()
        f.close()

cap = cv2.VideoCapture(0)
count=0
while True:
    success, img= cap.read()
    imgs = cv2.resize(img,(0,0), None, 0.25,0.25)
    imgs =cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
    faceCurframe = face_recognition.face_locations(imgs)
    encodeCurframe = face_recognition.face_encodings(imgs,faceCurframe)
    for encodeFace,faceloc in zip(encodeCurframe , faceCurframe):
        mathces = face_recognition.compare_faces(encodeListknown  , encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown , encodeFace)

        matchIndex = np.argmin(faceDis)

        if mathces[matchIndex]:
            name = className[matchIndex].upper()
            print(name)
            y1,x2,y2,x1= faceloc
            y1,x2,y2,x1= y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            if count<=10:
                attendance(name,count)
                count+=1
                print(count)


    cv2.imshow('Camera', img)
    if cv2.waitKey(10)==13:
        break
cap.release()
cv2.destroyAllWindows()
