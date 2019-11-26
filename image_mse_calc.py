import numpy as np
import utils


def main():
    
    img1 = utils.read_image('lenna-denoise.png')    
    img2 = utils.read_image('results/task2_result.jpg')
    
    error = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    error = error/float(img1.shape[0] * img2.shape[1])
    print(error)


main()