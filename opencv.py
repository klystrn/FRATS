import cv2
import face_recognition
import sqlite3
import numpy as np
'''
face_detector1 = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')

def videoCapture(device):
    if device.isOpened() is True:
        print("Webcam Opening...")

        countFrames = 0
        while True:
            try:
                status, frame = device.read()

                if not status:
                    break

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_detector1.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

                if len(faces) > 0:
                    face_x, face_y, face_w, face_h = faces[0]  # Assuming only one face is detected

                    face_roi = frame[face_y:face_y + face_h, face_x:face_x + face_w]

                    face_roi = cv2.resize(face_roi, (150, 150))

                    countFrames += 1
                else:
                    countFrames = 0

                cv2.imshow('Video', frame)

                key = cv2.waitKey(1)

                if key == ord(' ') or countFrames == 20:
                    img = cv2.imwrite('webcam_screenshot.jpg', frame)
                    print('>> Webcam image captured')
                    webcam.release()
                    img_new = cv2.imread('webcam_screenshot.jpg', cv2.IMREAD_ANYCOLOR)
                    print('>> Webcam image saved')
                    img_new = cv2.imshow("Captured Image", img_new)
                    print('>> Webcam image displayed')
                    cv2.waitKey(1000)
                    cv2.destroyAllWindows()
                    break

                elif key == ord('q'):
                    webcam.release()
                    break

            except(KeyboardInterrupt):
                print("Webcam turning off...")
                webcam.release()
                cv2.destroyAllWindows()
                break

def find_face_encodings(image_path):
    # reading image
    image = cv2.imread(image_path)
    # get face encodings from the image
    face_enc = face_recognition.face_encodings(image)
    # return face encodings
    print('\n', face_enc[0])
    return face_enc[0]

def compareFaces(encoding1, encoding2):
    # checking both images are same
    is_same = face_recognition.compare_faces([encoding1], encoding2)#[0]
    print(f"Is Same: {is_same}")
    if is_same:
        # finding the distance level between images
        distance = face_recognition.face_distance(encoding1, encoding2)
        distance = round(distance[0] * 100)

        # calcuating accuracy level between images
        accuracy = 100 - round(distance)
        print("The images are same")
        print(f"Accuracy Level: {accuracy}%")

        return True
    else:
        print("The images are not same")
        return False

#================ Main Program ================
UserName = input("what is the user name: ")
con = sqlite3.connect('FRATS.db', check_same_thread=False)
cur = con.cursor()
cur.execute('SELECT Encoding FROM OpenCV INNER JOIN Image ON OpenCV.ImageID = Image.ID WHERE Image.UserName = ?',( UserName,))
result = cur.fetchone()
encoding2 = np.fromstring(result[0])
#encoding2.append() 
webcam = cv2.VideoCapture(0)
videoCapture(webcam)

# getting face encodings for first image
image1 = find_face_encodings("webcam_screenshot.jpg")[0]
print(type(image1))
print(type(encoding2))
# getting face encodings for second image
#image2  = find_face_encodings("img2.jpg") #call the facial encoding data from database and replace this

compareFaces(image1, image2)
'''
face_detector1 = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')

def videoCapture(device):
    if device.isOpened() is True:
        print("Webcam Opening...")

        countFrames = 0
        while True:
            try:
                status, frame = device.read()

                if not status:
                    break

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_detector1.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

                if len(faces) > 0:
                    face_x, face_y, face_w, face_h = faces[0]  # Assuming only one face is detected

                    face_roi = frame[face_y:face_y + face_h, face_x:face_x + face_w]

                    face_roi = cv2.resize(face_roi, (150, 150))

                    countFrames += 1
                else:
                    countFrames = 0

                cv2.imshow('Video', frame)

                key = cv2.waitKey(1)

                if key == ord(' ') or countFrames == 20:
                    img = cv2.imwrite('webcam_screenshot.jpg', frame)
                    print('>> Webcam image captured')
                    webcam.release()
                    img_new = cv2.imread('webcam_screenshot.jpg', cv2.IMREAD_ANYCOLOR)
                    print('>> Webcam image saved')
                    img_new = cv2.imshow("Captured Image", img_new)
                    print('>> Webcam image displayed')
                    cv2.waitKey(1000)
                    cv2.destroyAllWindows()
                    break

                elif key == ord('q'):
                    webcam.release()
                    break

            except(KeyboardInterrupt):
                print("Webcam turning off...")
                webcam.release()
                cv2.destroyAllWindows()
                break

def find_face_encodings(image_path):
    # reading image
    image = cv2.imread(image_path)
    # get face encodings from the image
    face_enc = face_recognition.face_encodings(image)
    # return face encodings
    print('\n', face_enc[0])
    return face_enc[0]

def compareFaces(encoding1, encoding2):
    # checking both images are same
    is_same = face_recognition.compare_faces([encoding1], encoding2)[0]
    print(f"Is Same: {is_same}")
    if is_same:
        # finding the distance level between images
        distance = face_recognition.face_distance([encoding1], encoding2)
        distance = round(distance[0] * 100)

        # calcuating accuracy level between images
        accuracy = 100 - round(distance)
        print("The images are same")
        print(f"Accuracy Level: {accuracy}%")

        return True
    else:
        print("The images are not same")
        return False

#================ Main Program ================
webcam = cv2.VideoCapture(0)
videoCapture(webcam)
UserName = input("what is the user name: ")
con = sqlite3.connect('FRATS.db', check_same_thread=False)
cur = con.cursor()
cur.execute('SELECT Encoding FROM OpenCV INNER JOIN Image ON OpenCV.ImageID = Image.ID WHERE Image.UserName = ?',( UserName,))
result = cur.fetchone()
encoding2 = np.fromstring(result[0])
encoding2 = np.array(np.matrix(result[0]).reshape(1,128))

# getting face encodings for first image
image1 = find_face_encodings("webcam_screenshot.jpg")
# getting face encodings for second image
#image2  = find_face_encodings("img2.jpg") #call the facial encoding data from database and replace this
print(encoding2) 
print(image1)
compareFaces(image1, encoding2)

