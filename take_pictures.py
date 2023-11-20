import cv2
from time import sleep

def take_pic(i: int):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(f'pic_{i}.jpg', frame)
    cv2.imshow(f'pic_{i}.jpg', frame)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    while True:
        i = 0
        take_pic(i)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        sleep(5)
