# This code will filter and keep the images with 2 clear red lines (the path) 
# appear in the bottom half of the images, indicating the Donkeycar is on track
# and the image is good for training the model

import numpy as np
import cv2
import os

height = 120
width = 160
number_of_image = 30000

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    channel_count = 3
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# The path are usually at the bottom half of the image
region_of_interest_vertices = [
    (0, height),
    (0, height * 0.5),
    (width, height * 0.5),
    (width, height),
]

boundaries = [
	([30, 25, 50], [100, 100, 160]) # red pixel range
]

for i in range(number_of_image):
    area = height * width
    path = f'raw/data_4/images/{i}_cam_image_array_.jpg'
    image = cv2.imread(path)
    filename = f'{i}_cam_image_array_.jpg'
    for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
	# find the colors within the specified boundaries and apply
	# the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)

    cropped_image = region_of_interest(
        output,
        np.array([region_of_interest_vertices], np.int32),  
    )

    for row in range(120):
        for col in range(160):
            # check for black pixels
            if (cropped_image[row][col][0] == 0 and\
            cropped_image[row][col][1] == 0 and\
            cropped_image[row][col][2] == 0) or\
            (not (cropped_image[row][col][2] > max(cropped_image[row][col][1], cropped_image[row][col][0]))):
                area -= 1

    if area >= 900: # lots of red pixels
        os.rename(path, 'raw/good_data/' + filename) # used for training
    else:
        os.rename(path, 'raw/bad_data/' + filename) # bad images are stored to filter out the correspoding entries in catalog files

