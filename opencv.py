import cv2

face_detector1 = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
eye_dectector1 = cv2.CascadeClassifier('data/haarcascades/haarcascade_eye.xml')

def eyeDetect(ex1, ey1, ew1, eh1, roi_color):
    cv2.rectangle(roi_color, (ex1, ey1), (ex1 + ew1, ey1 + eh1), (0, 255, 0), 2)
    print(f'X:{ex1}, Y:{ey1}')
    print(f'W:{ew1}, H:{eh1}')
    print('-----------------')

    return True

def videoCapture():
    webcam = cv2.VideoCapture(0)

    if webcam.isOpened() is True:
        print("Webcam Opening...")

        while True:
            try:
                print('------------- NEW FRAME -------------')
                _, frame = webcam.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_detector1.detectMultiScale(gray, 1.1, 4)

                faceHeightHalf = 0

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]
                    eyes = eye_dectector1.detectMultiScale(roi_gray)

                    print(f'Face = X:{x} Y:{y}')

                countEyes = 0
                for (ex, ey, ew, eh) in eyes:
                    if eyeDetect(ex, ey, ew, eh, roi_color) is True:
                        countEyes += 1
                    if countEyes > 2:
                        print('more than 2 eyes detected')
                        break

                cv2.imshow("Capturing Video...", frame)
                print(f'Number of Eyes: {countEyes}')

                key = cv2.waitKey(1)

                if key == ord(' '):
                    img = cv2.imwrite('webcam_screenshot.png', frame)
                    print('>> Webcam image captured')
                    webcam.release()
                    img_new = cv2.imread('webcam_screenshot.png', cv2.IMREAD_ANYCOLOR)
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


videoCapture()