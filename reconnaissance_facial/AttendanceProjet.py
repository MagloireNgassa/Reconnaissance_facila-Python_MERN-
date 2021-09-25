# Load libraries
import urllib.request as urllib2

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import requests

import googletrans
import speech_recognition as sr
import gtts
import playsound
recognizer = sr.Recognizer()
translator = googletrans.Translator()
input_lang = 'fr-FR'
output_lang = 'en'


#make transmission to the database
# def transmission(name,date,time):
#     picture = ''
#     for pick in myList:
#         Names = os.path.splitext(pick)[0]
#         print(Names)
#         if Names.upper() == name:
#             picture = pick
#             break
#
#     url = 'http://localhost:3535/presence'
#     myobj = {'nom': name,'date':date,'time':time,'photo':picture}
#     x = requests.post(url, data = myobj)
#
#     return(x.text)


def transmission(name, date, time):
    url = 'http://localhost/python_attendance/attendance.php'
    myobj = {'nom': name, 'date': date, 'heure': time, 'statut': 'entré', 'score': 1}
    x = requests.post(url, data=myobj)

    print(x.text)
    return(x.text)



# Mark Attendance
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        # retrieve existing name
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d')
            hrString = now.strftime('%H: %M: %S')
            print(dtString)
            print(hrString)
            result = transmission(name, dtString,hrString)
            print("retour du php: " + result)
            f.writelines(f'\n{name}, {dtString}')
            print(name, " Sucessfully identified!")
            text = name + " Successfully identified!"
            translated = translator.translate(text, dest=output_lang)
            print(translated.text)
            converted_audio = gtts.gTTS(translated.text, lang=output_lang)

            converted_audio.save(f'confirm{name}.mp3')
            playsound.playsound(f'confirm{name}.mp3')
            print(googletrans.LANGUAGES)


# Compute encoding of images
def findEncoding(myImgs): # myImgs is the list of images (matrix of pixels)
    encodeList = []
    for myimg in myImgs:
        img = cv2.cvtColor(myimg, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList




# Chemin vers notre dossier d'images
path = "ImagesBasic"
images = [] # List of images from the folder
classNames = []# list of images' names
# Grab the list of images in the folder
myList = os.listdir(path)# recuperation de la liste des fichier du dossier vers le tableau myList
# print(myList)
# Read images fro the folder
for cl in myList:
    # print(f'{path}/{cl}')
    curImg = cv2.imread(f'{path}/{cl}')
    #print(curImg)
    print(cl)
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
#print(myList)
#print(classNames)
#print (images)

# Encode all the images
encodeListFinal = findEncoding(images)
#print(encodeListFinal)
print("Images were encoded successfully!")

# Read from camera
cap = cv2.VideoCapture(0)
while True:# Get the frame one by one
    success , img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    # (0,0): original image
    # None: define any pixel size
    # scale: 1/4 of the size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    # Find face location of our webcam
    facesCurFrame = face_recognition.face_locations(imgS)
    # Encode face
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListFinal, encodeFace)
        faceDis = face_recognition.face_distance(encodeListFinal, encodeFace)
        # print(match)
        # print(faceDis)
        # return the element with smallest distance
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper() # retrieve name and convert in UpperCase
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+10, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

            

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)







