import cv2
import numpy as np
from imutils.convenience import grab_contours

# Load in input images from the web
orig_img = cv2.imread("images/species1.jpg")

cap = cv2.VideoCapture(0)


""" Program to match shapes"""
def match_shapes(orig_img):
    # Read in the images for matching
    species = ["species_" + name for name in ["A", "B", "C", "D"]]
    shape_images = [cv2.cvtColor(cv2.imread("shape_images/" + image_name + ".png"), cv2.COLOR_BGR2GRAY) for image_name in species]
    shape_contours = []

    img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
    blockKernel = np.ones((3, 3))  # Should be a very aggressive erode

    # Morphological operators to clean up the image
    _, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Binarized Img", img)
    cv2.waitKey(1)

    img = cv2.erode(img, blockKernel)
    img = cv2.dilate(img, blockKernel)

    # Find contour for shape images that we already have
    for shape_img in shape_images:
        _, binary_img = cv2.threshold(shape_img.copy(), 200, 255, cv2.THRESH_BINARY_INV)
        contours = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = grab_contours(contours)
        shape_contours.append(contours[0])  # Assume that the first contour is the desired one
        # Good for debugging the shape contours
        # final_img = np.zeros((binary_img.shape[0], binary_img.shape[1], 3))
        # final_img[:,:,2] = binary_img
        # cv2.drawContours(final_img, contours[0], -1, (0,255,0, 1))
        # cv2.imshow("adsfasd", final_img)
        # cv2.waitKey(-1)

    # Find contours for input image
    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = grab_contours(contours)

    cv2.drawContours(orig_img, contours, -1, (0, 255, 0), 1)

    for potential_shape in contours:
        probable_species = (2000, None)  # distance (2000 is huge), species name

        cv2.drawContours(orig_img, [potential_shape], -1, (255, 0, 0), 2)
        shape_moments = cv2.moments(potential_shape)
        hu_shape_moments = cv2.HuMoments(shape_moments)

        for shape_contour, species_name in zip(shape_contours, species):
            potential_shape_moments = cv2.moments(shape_contour)
            potential_hu_moments = cv2.HuMoments(potential_shape_moments)
            dist = sum([(x - y)**2 for x,y in zip(potential_hu_moments[0:5], hu_shape_moments[0:5])])

            #dist = cv2.matchShapes(potential_shape, shape_contour, cv2.CONTOURS_MATCH_I3, 0)
            probable_species = (dist, species_name) if dist < probable_species[0] else probable_species
        if not probable_species[1]:
            break


        moments = cv2.moments(potential_shape)
        shape_centerX = int((moments["m10"] / moments["m00"]))
        shape_centerY = int((moments["m01"] / moments["m00"]))


        cv2.putText(orig_img, probable_species[1], (shape_centerX, shape_centerY), cv2.FONT_HERSHEY_COMPLEX,
                    .5, (0, 0, 255), 2)

        # Display the output
        cv2.imshow("Shapes", orig_img)
        cv2.waitKey(1)

while True:
    ret, frame = cap.read()
    match_shapes(frame)

