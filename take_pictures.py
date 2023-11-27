import cv2
from picamera2 import Picamera2
from time import sleep

def take_pictures():
    picam = Picamera2()
    picam.preview_configuration.main.size=(1280/2, 720/2)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("capture")
    picam.start()

    i = 1
    while True:
        # Take a picture if p is pressed and break program if q is pressed
        frame = picam.capture_array()
        cv2.imshow("picam", frame[::-1])
        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.imwrite("images_checkers/image"+str(i)+".jpg", frame[::-1])
            i += 1
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    take_pictures()    
