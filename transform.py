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
    
    output[y + width - shift:y + 2 * width - shift, x:x + width] = img[y + width:y + 2 * width, x:x + width]
    output[y + width:y + 2 * width, x + width - shift:x + 2 * width - shift] = img[y + width:y + 2 * width, x + width:x + 2 * width]
    output[y + shift:y + width + shift, x + width:x + 2 * width] = img[y:y + width, x + width:x + 2 * width]
    output[y:y + width, x + shift:x + width + shift] = img[y:y + width, x:x + width]

def v_flip_with_steps(img, output, y, width, shift):

    output[y + shift: y + width + shift, 0:img_dim] = img[y: y + width, 0:img_dim]
    output[y + width - shift: y + 2 * width - shift, 0:img_dim] = img[y + width: y + 2 * width, 0:img_dim]
    
def h_flip_with_steps(img, output, x, width, shift):

    output[0:img_dim, x + shift:x + width + shift] = img[0:img_dim, x:x + width]
    output[0:img_dim, x + width - shift:x + 2 * width - shift] = img[0:img_dim, x + width:x + 2 * width]

if len(sys.argv) < 3:
    print("Usage: transform.py <input_image.png> <output_file.mp4> optional: <transform_type>")
    print("\t transform_type = 0: rotation")
    print("\t transform_type = 1: vertical flip")
    print("\t transform_type = 2: horizontal flip")
    print("\t transform_type = 3: vertical+horizontal flip")
    print("Note that the image must have dimensions N x N where N is a power of 2")
    sys.exit()

transform_type = 0

if len(sys.argv) >= 4:
    transform_type = int(sys.argv[3])

#read in the image
file_name = sys.argv[1]
image = cv.imread(file_name)
img_dim = image.shape[0]

#make a video writer
out_file_name = sys.argv[2]
out = cv.VideoWriter(out_file_name, cv.VideoWriter_fourcc('m','p','4','v'), 30, (img_dim, img_dim))

for i in range(30):
    out.write(image)

#rotate the image 4 times
if transform_type < 3:
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
            
                if transform_type == 0:
                    for x in range(0, img_dim, 2 * width):
                        for y in range(0, img_dim, 2 * width):
                            rotate_with_steps(image, output_canvas, x, y, width, shift)
                elif transform_type == 1:
                    for y in range(0, img_dim, 2 * width):
                        v_flip_with_steps(image, output_canvas, y, width, shift)
                elif transform_type == 2:
                    for x in range(0, img_dim, 2 * width):
                        h_flip_with_steps(image, output_canvas, x, width, shift)
                
                cv.imshow('output', output_canvas)
                cv.waitKey(1)
                
                out.write(output_canvas)
            
            image = np.copy(output_canvas)
            width = width // 2
else:
    for rotations in range(4):
        width = img_dim // 2
        number_of_frames = 2 * int(math.log2(img_dim))

        while width > 1:
            
            number_of_frames -= 2
            number_of_frames = max(1, number_of_frames)

            #create the sliding animation by gradually moving the tiles
            
            #first flip the horizontal direction
            for i in range(0, number_of_frames):
            
                output_canvas = np.copy(image)
                shift = (width * (i + 1)) // number_of_frames
            
                for x in range(0, img_dim, 2 * width):
                    h_flip_with_steps(image, output_canvas, x, width, shift)
                
                cv.imshow('output', output_canvas)
                cv.waitKey(1)
                
                out.write(output_canvas)
            
            image = np.copy(output_canvas)
            
            #next flip the vertical direction
            for i in range(0, number_of_frames):
            
                output_canvas = np.copy(image)
                shift = (width * (i + 1)) // number_of_frames
            
                for y in range(0, img_dim, 2 * width):
                    v_flip_with_steps(image, output_canvas, y, width, shift)
                
                cv.imshow('output', output_canvas)
                cv.waitKey(1)
                
                out.write(output_canvas)
            
            image = np.copy(output_canvas)
            width = width // 2

for i in range(30):
    out.write(image)

out.release()


