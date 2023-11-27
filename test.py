import cv2
from picamera2 import Picamera2

def stream_video():
    picam = Picamera2()
    picam.preview_configuration.main.size=(int(1280/2), int(720/2))
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    while True:
        frame = picam.capture_array()
        cv2.imshow("picam", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)[::-1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()