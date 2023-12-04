import cv2
import numpy as np
import matplotlib.pyplot as plt
from picamera2 import Picamera2
from time import sleep


def password_boards() -> (np.ndarray, np.ndarray, np.ndarray):
    
    # Boards to be used as password
    board_zeros = np.zeros((8, 8), dtype=int)

    # Board 1 - Initial state
    board1 = board_zeros.copy()
    board1[0] = [0, -1, 0, -1, 0, -1, 0, 0]
    board1[-1] = [1, 0, 1, 0, 1, 0, 1, 0]

    # Board 2 - Initial state with a 0 in (0,-1)
    board2 = board1.copy()
    board2[0, -1] = 0

    # Board 3 - Board2 with a 0 in (-1, 0)
    board3 = board2.copy()
    board3[-1, 0] = 0

    return board1, board2, board3


def password_unlock(current_matrix, security_level=0):

    boards = password_boards()
    
    if security_level == 0 and np.array_equal(current_matrix, boards[0]):
        security_level += 1
        print('Security level 1')
    elif security_level == 1 and np.array_equal(current_matrix, boards[1]):
        security_level += 1
        print('Security level 2')
    elif security_level == 2 and np.array_equal(current_matrix, boards[2]):
        security_level += 1
        print('Security level 3')
    
    return security_level


if __name__ == "__main__":
    boards = password_boards()
    print(boards[0])
    print(boards[1])
    print(boards[2])