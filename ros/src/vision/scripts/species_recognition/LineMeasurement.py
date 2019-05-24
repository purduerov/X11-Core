import cv2
import numpy as np

from imutils import grab_contours

""" Detects corners in an image and a blue line. The program uses the known distance between corners to determine
the length of the line"""

# Read in a test image
orig_img = cv2.imread("images/sampleLine1.png")

hsvImage = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
redMask = cv2.add(cv2.inRange(hsvImage, (0, 150, 45), (13, 255, 255)),
                  cv2.inRange(hsvImage, (150, 150, 45), (180, 255, 255)))
blueMask = cv2.inRange(hsvImage, (100, 100, 45), (140, 255, 255))


# Locate Horizontal and vertical lines
_, lineMask = cv2.threshold(cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY), 25, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones(3, 3)
lineMask = cv2.erode(lineMask, kernel)
lineMask = cv2.dilate(lineMask, kernel)
lines = cv2.HoughLines(lineMask, 1, np.pi/180, 200)

y_intercepts = []
x_intercepts = []

# Go through each of the detected lines for measurement
for rho, theta in lines[:, 0, :]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))


    # Line is horizontal
    if theta < np.pi /4:
        x_intercepts.append(np.cos(theta) * rho)
    else:
        y_intercepts.append(np.sin(theta) * rho)


    cv2.line(orig_img,(x1,y1),(x2,y2),(0,255,0),2)

ratio = 1
intersection = False
# If we found more than one vertical line
if len(x_intercepts) > 1:
    # If there's an x and y intercept then there's a corner!
    if len(y_intercepts):
        c1 = [x_intercepts[0], y_intercepts[0]]
        c2 = [x_intercepts[1], y_intercepts[0]]
        dist = np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        known_dist = .30
        ratio = known_dist / dist
        intersection = True
elif len(y_intercepts) > 1:
    if len(x_intercepts):
        c1 = [x_intercepts[0], y_intercepts[0]]
        c2 = [x_intercepts[0], y_intercepts[1]]
        dist = np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        known_dist = .30
        ratio = known_dist / dist
        intersection = True

contours = cv2.findContours(blueMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = grab_contours(contours)

# If we found any contours
if len(contours):
    width, height = cv2.minAreaRect(contours[0])[1]
    centerX, centerY = cv2.minAreaRect(contours[0])[0]
    length = width if width > height else height
    vertical = True if height > width else False

    # Only save measurement while camera is looking straight on (error less than 30 px)
    if not vertical and intersection and abs(centerX - blueMask.shape[1] / 2) < 30:
        print length
        print "Actual distance: " + str(length * ratio)
    elif vertical and intersection and abs(centerY - blueMask.shape[0] / 2) < 30:
        print length
        print "Actual distance: " + str(length * ratio)


cv2.imshow("RedMask", orig_img)
cv2.waitKey(-1)
