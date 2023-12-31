import cv2
import numpy as np
import matplotlib.pyplot as plt
from picamera2 import Picamera2
from time import sleep
import password

def get_chessboard(img, corners, nx, ny):
    """
    Find the chessboard corners in the given image.
    :param img: the image to find the chessboard corners in
    :param nx: the number of corners in the x direction
    :param ny: the number of corners in the y direction
    :return: the image with the chessboard corners drawn on it
    """


    # Draw and display the corners
    # cv2.drawChessboardCorners(img, (nx, ny), corners, ret)

    # Choose offset from image corners to plot detected corners
    # This should be chosen to present the result at the proper aspect ratio
    # My choice of 100 pixels is not exact, but close enough for our purpose here
    offset = 100  # offset for dst points

    # I want the image size to be squared so I can warp to a square
    # The destination points are chosen to be at this size
    img_size = (800, 800)

    # For source points I'm grabbing the outer four detected corners
    src = np.float32([corners[0], corners[nx - 1], corners[-1], corners[-nx]])

    # For destination points, I'm choosing the four corners of the square
    # These are in the order top-left, top-right, bottom-right, bottom-left
    dst = np.float32([
        [offset, offset],
        [img_size[0] - offset, offset],
        [img_size[0] - offset, img_size[1] - offset],
        [offset, img_size[1] - offset]
        ])

    # Given src and dst points, calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(src, dst)

    # Warp the image using OpenCV warpPerspective()
    warped = cv2.warpPerspective(img, M, img_size)

    return warped


def chessboard_to_matrix(chessboard_image, chessboard_shape):
    """
    params:
        chessboard_image: image of the chessboard
        chessboard_shape: tuple of (rows, cols) of the chessboard
    returns:
        matrix: array of shape (rows * cols, 2) with the coordinates of the chessboard corners
    """
    dx, dy = chessboard_image.shape[0] // chessboard_shape[0], chessboard_image.shape[1] // chessboard_shape[1]
    
    chessboard_matrix = np.zeros(chessboard_shape)

    for j in range(chessboard_shape[0]):
        for i in range(chessboard_shape[1]):
                # I want to check in each box of the chessboard whether there is a circle
                # If there is a circle, I will put a 1 in the chessboard_matrix
                # If there is no circle, I will put a 0 in the chessboard_matrix
                chessboard_image_box = chessboard_image[j*dy:(j+1)*dy, i*dy:(i+1)*dy]
                # Convert to grayscale
                image_gray = cv2.cvtColor(chessboard_image_box, cv2.COLOR_BGR2GRAY)
                # I will use HoughCircles to detect the circles
                circles = cv2.HoughCircles(image_gray, cv2.HOUGH_GRADIENT, 1, 20,
                                            param1=50, param2=30, minRadius=0, maxRadius=0)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    x, y, radius = circles[0][0]
                    # Get the red channel only from the circle
                    red_channel = chessboard_image_box[y-radius:y+radius, x-radius:x+radius, 2]
                    mean_red = np.mean(red_channel)

                    if mean_red > 180:
                        chessboard_matrix[j][i] = -1
                    else:
                        chessboard_matrix[j][i] = 1

                    # Draw the circle in the chessboard_image
                    # Circumference
                    cv2.circle(chessboard_image, (x+i*dy, y+j*dy), radius, (0, 255, 0), 2)
                    # Center
                    cv2.circle(chessboard_image, (x+i*dy, y+j*dy), 2, (0, 0, 255), 3)
                else:
                    chessboard_matrix[j][i] = 0

    return chessboard_matrix


def main():

    picam = Picamera2()
    picam.preview_configuration.main.size=(int(1280), int(720))
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("capture")
    picam.start()

    chessboard_states = []
    security_level = 0
    nx, ny = 8, 8

    boards = password.password_boards()
    chessboard_matrix = np.zeros((8, 8))

    # While the two numpy arrays are not equal
    while not np.array_equal(chessboard_matrix, boards[0]):
        frame = picam.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(frame_gray, (nx-1, ny-1), None)
        if ret:
            frame_cropped = get_chessboard(frame, corners, 7, 7)
            if frame_cropped is not None:
                chessboard_matrix = chessboard_to_matrix(frame_cropped, (8, 8))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    while True:
        frame = picam.capture_array()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_cropped = get_chessboard(frame, corners, 7, 7)
        if frame_cropped is not None:
            chessboard_matrix = chessboard_to_matrix(frame_cropped, (8, 8))
            if chessboard_matrix is not None:
                # If the chessboard state found is not already in the list of chessboard states
                if not any(np.array_equal(chessboard_matrix, board) for board in chessboard_states):
                    chessboard_states.append(chessboard_matrix)

                    if security_level < 3:
                        security_level = password.password_unlock(chessboard_matrix, security_level)
            cv2.imshow("picamera", frame_cropped)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    


if __name__ == "__main__":
    main()