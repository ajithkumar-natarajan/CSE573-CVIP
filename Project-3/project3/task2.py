"""
Denoise Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to denoise image using median filter.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are suggested to use utils.zero_pad.
"""


import utils
import numpy as np
import json

def median_filter(img):
    """
    Implement median filter on the given image.
    Steps:
    (1) Pad the image with zero to ensure that the output is of the same size as the input image.
    (2) Calculate the filtered image.
    Arg: Input image. 
    Return: Filtered image.
    """
    # TODO: implement this function.
    filter_size = 3
    pw = filter_size//2
    padded_img = utils.zero_pad(img, pw, pw)
    output = np.zeros((len(img),len(img[0])))
    
    neighbours = list()
    for i in range(1, len(output)+1):
        for j in range(1, len(output[0])+1):
            for k in range(i-pw, i+pw+1):
                for l in range(j-pw, j+pw+1):
                    neighbours.append(padded_img[k, l])
            neighbours.sort()
            output[i-1][j-1] = neighbours[4]
            neighbours.clear()

    return output.astype(np.uint8)



def mse(img1, img2):
    """
    Calculate mean square error of two images.
    Arg: Two images to be compared.
    Return: Mean square error.
    """    
    # TODO: implement this function.
    error = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    error = error/float(img1.shape[0] * img2.shape[1])

    return error
    

if __name__ == "__main__":
    img = utils.read_image('lenna-noise.png')
    gt = utils.read_image('lenna-denoise.png')

    result = median_filter(img)
    error = mse(gt, result)

    with open('results/task2.json', "w") as file:
        json.dump(error, file)
    utils.write_image(result,'results/task2_result.jpg')