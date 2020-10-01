import numpy as np
import cv2 as cv
import sys
import math

"""
The following rotate function is only included for reference and is not called.
This shows how the recursion works, but does not provide any sort of interesting animation.
"""
def rotate(img, x, y, width):

    width = width // 2
        
    #divides the image into four region and slides them clockwise
    temp = np.copy(img[y:y + width, x:x + width])
    
    img[y:y + width, x:x + width] = img[y + width:y + 2 * width, x:x + width]
    img[y + width:y + 2 * width, x:x + width] = img[y + width:y + 2 * width, x + width:x + 2 * width]
    img[y + width:y + 2 * width, x + width:x + 2 * width] = img[y:y + width, x + width:x + 2 * width]
    img[y:y + width, x + width:x + 2 * width] = temp
    
    if width > 1:
        #recusively rotating the tiles
        rotate(img, x, y, width)
        rotate(img, x + width, y, width)
        rotate(img, x + width, y + width, width)
        rotate(img, x, y + width, width)

def rotate_with_steps(img, output, x, y, width, shift):
    
    temp = np.copy(img[y:y + width, x:x + width])
    
    output[y + width - shift:y + 2 * width - shift, x:x + width] = img[y + width:y + 2 * width, x:x + width]
    output[y + width:y + 2 * width, x + width - shift:x + 2 * width - shift] = img[y + width:y + 2 * width, x + width:x + 2 * width]
    output[y + shift:y + width + shift, x + width:x + 2 * width] = img[y:y + width, x + width:x + 2 * width]
    output[y:y + width, x + shift:x + width + shift] = temp

def is_power_of_two(n):
    return (n != 0) and (n & (n-1) == 0)

def yes_or_no(question):
    while True:
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

if len(sys.argv) != 3:
    print("Usage: rotate.py <input_image> <output_file>")
    print("Note that the image must have dimensions N x N where N is a power of 2")
    sys.exit()


#read in the image
file_name = sys.argv[1]
image = cv.imread(file_name)

#check if image is of the right size
if not is_power_of_two(min(image.shape[0], image.shape[1])):
    print("The image you have provided does not have dimensions N x N where N is a power of 2.")
    closest_valid_dimension = 2**round(math.log(min(image.shape[0], image.shape[1]), 2))
    #prompt user to either resize image to closest NxN where N is a power of 2
    if yes_or_no("Would you like to try to automatically resize this image to the closest functional dimensions: {}x{}?".format(closest_valid_dimension, closest_valid_dimension)):
        image = cv.resize(image, (closest_valid_dimension, closest_valid_dimension))
    else:
        #user does not want to resize
        #since program does not run with improperly sized images, exit
        print("Exiting...")
        sys.exit()

img_dim = image.shape[0]

#make a video writer
out_file_name = sys.argv[2]
out = cv.VideoWriter(out_file_name, cv.VideoWriter_fourcc('m','p','4','v'), 30, (img_dim, img_dim))

#rotate the image 4 times
for rotations in range(4):

    width = img_dim // 2
    number_of_frames = 2 * int(math.log2(img_dim))

    while width > 1:
        
        number_of_frames -= 2
        number_of_frames = max(1, number_of_frames)

        #create the sliding animation by gradually moving the tiles
        for i in range(0, number_of_frames):
        
            output_canvas = np.copy(image)
            shift = (width * (i + 1)) // number_of_frames
        
            for x in range(0, img_dim, 2 * width):
                for y in range(0, img_dim, 2 * width):
                    rotate_with_steps(image, output_canvas, x, y, width, shift)
                    
            cv.imshow('output', output_canvas)
            cv.waitKey(1)
            
            out.write(output_canvas)
        
        image = np.copy(output_canvas)
        width = width // 2
    
out.release()


