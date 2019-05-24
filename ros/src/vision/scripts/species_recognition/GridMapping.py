import cv2
import numpy as np
from imutils import grab_contours

# Sample input to exercise code
cap = cv2.VideoCapture("images/lineFollow1.mp4")

# State names
PRECROSS_A = "precrossA"
CROSS_AtoB = "cross_AtoB"
CROSS_BtoA = "cross_BtoA"
PRECROSS_B = "precrossB"
IDLE = "idle"


# State memory
last_state_horizontal = None
last_state_vertical = None


""" OpenCV has a predisposition to find a lot of lines on top of eachother, this code should limit that"""
def find_strong_lines(weak_lines, thresh = 400):

    current_lines = []
    for rho, theta in weak_lines:
        # Make sure the line is oriented positively
        if rho < 0:
            rho *= -1
            theta -= np.pi

        if len(current_lines) == 0:
            current_lines.append((rho, theta))
            continue

        np_current_lines = np.asarray(current_lines)
        close_rho = np.isclose(rho, np_current_lines[:, 0], atol=thresh)  # lines should be far from each other
        close_theta = np.isclose(theta, np_current_lines[:, 1], atol=np.pi/4)
        close_lines = np.all([close_rho, close_theta], axis=0)

        if not any(close_lines):
           current_lines.append((rho, theta))

    return current_lines


""" Figure out what state we are in and if the new frame merits a change to a new position in the grid """
def update_state(frame, oldX, oldY):
    global last_state_horizontal, last_state_vertical

    curr_x = oldX
    curr_y = oldY

    # Get dimension of image measurement bands
    bandwidth = .15 * frame.shape[0]
    bandheight = .15 * frame.shape[1]

    _, gridMask = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 25, 255, cv2.THRESH_BINARY_INV)

    # Clean out noise from teh image
    kernel = np.ones((3, 3))
    gridMask = cv2.erode(gridMask, kernel)
    gridMask = cv2.dilate(gridMask, kernel)
    weak_lines = cv2.HoughLines(gridMask, 1, np.pi/180, 200)

    # if there aren't any lines then don't do anything
    if weak_lines is None:
        return curr_x, curr_y

    # Remove duplicate detections from the detected lines
    lines = find_strong_lines(weak_lines[:, 0, :], thresh=int(frame.shape[0]* .3))

    # Go through each of the lines and determine if the line is the cross bands
    for rho, theta in lines:

        # Code for displaying located lines (Debugging purposes)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("GridMapping", frame)
        cv2.waitKey(1)  # Show the output image

        # Line is vertical
        if theta < np.pi/4:
            x_intercept = rho  # Not necessarily true but small angle approx

            start_precrossA = frame.shape[1] / 2 - bandwidth/2 - bandwidth
            end_precrossA = frame.shape[1] / 2 - bandwidth/2

            start_cross = frame.shape[1]/2 - bandwidth/2
            end_cross = frame.shape[1]/2 + bandwidth/2

            start_precrossB = frame.shape[1]/2 + bandwidth/2
            end_precrossB = frame.shape[1] + bandwidth/2 + bandwidth

            # Check current State
            current_state = None
            if start_precrossA < x_intercept < end_precrossA:
                current_state = PRECROSS_A
            elif start_cross <= x_intercept <= end_cross:
                if last_state_vertical == PRECROSS_A:
                    current_state = CROSS_AtoB
                elif last_state_vertical == PRECROSS_B:
                    current_state = CROSS_BtoA
            elif start_precrossB < x_intercept < end_precrossB:
                current_state = PRECROSS_B

            # Check for a state transition indicating to the left
            if last_state_vertical == CROSS_AtoB and current_state == PRECROSS_B:
                curr_x = oldX - 1
            if last_state_vertical == CROSS_BtoA and current_state == PRECROSS_A:
                curr_x = oldX + 1
            last_state_vertical = current_state if current_state is not None else last_state_vertical

        # Line is horizontal
        elif theta > np.pi/4:
            y_intercept = rho

            start_precrossA = frame.shape[0] / 2 - bandheight/2 - bandheight
            end_precrossA = frame.shape[0] / 2 - bandheight/2

            start_cross = frame.shape[0]/2 - bandheight/2
            end_cross = frame.shape[0]/2 + bandheight/2

            start_precrossB = frame.shape[0]/2 + bandheight/2
            end_precrossB = frame.shape[0]/2 + bandheight/2 + bandheight

            current_state = None
            if start_precrossA < y_intercept < end_precrossA:
                current_state = PRECROSS_A
            elif start_cross <= y_intercept <= end_cross:
                if last_state_horizontal == PRECROSS_A:
                    current_state = CROSS_AtoB
                elif last_state_horizontal == PRECROSS_B:
                    current_state = CROSS_BtoA
            elif start_precrossB < y_intercept < end_precrossB:
                current_state = PRECROSS_B

            # Check for a state transition indicating to the left
            if last_state_horizontal == CROSS_AtoB and current_state == PRECROSS_B:
                curr_y = oldY - 1
            if last_state_horizontal == CROSS_BtoA and current_state == PRECROSS_A:
                curr_y = oldY + 1
            last_state_horizontal = current_state if current_state is not None else last_state_horizontal

    return curr_x, curr_y


if __name__ == "__main__":
    # Program run time loop
    oldX = 0
    oldY = 0
    ret, camera_frame = cap.read()
    while camera_frame is not None:
        X, Y = update_state(camera_frame, oldX, oldY)
        oldX = X
        oldY = Y
        print "Current X: " + str(X) + " Current Y: " + str(Y)
        ret, camera_frame = cap.read()

