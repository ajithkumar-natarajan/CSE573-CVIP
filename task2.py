"""
Template Matching
(Due date: Sep. 25, 3 P.M., 2019)

The goal of this task is to experiment with template matching techniques, i.e., normalized cross correlation (NCC).

Please complete all the functions that are labelled with '# TODO'. When implementing those functions, comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in 'utils.py'
and the functions you implement in 'task1.py' are of great help.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
"""


import argparse
import json
import os

import utils
from task1 import *


def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img-path",
        type=str,
        default="./data/proj1-task2.jpg",
        help="path to the image")
    parser.add_argument(
        "--template-path",
        type=str,
        default="./data/proj1-task2-template.jpg",
        help="path to the template"
    )
    parser.add_argument(
        "--result-saving-path",
        dest="rs_path",
        type=str,
        default="./results/task2.json",
        help="path to file which results are saved (do not change this arg)"
    )
    args = parser.parse_args()
    return args

def norm_xcorr2d(patch, template):
    """Computes the NCC value between a image patch and a template.

    The image patch and the template are of the same size. The formula used to compute the NCC value is:
    sum_{i,j}(x_{i,j} - x^{m}_{i,j})(y_{i,j} - y^{m}_{i,j}) / (sum_{i,j}(x_{i,j} - x^{m}_{i,j}) ** 2 * sum_{i,j}(y_{i,j} - y^{m}_{i,j})) ** 0.5
    This equation is the one shown in Prof. Yuan's ppt.

    Args:
        patch: nested list (int), image patch.
        template: nested list (int), template.

    Returns:
        value (float): the NCC value between a image patch and a template.
    """
    # raise NotImplementedError

    templatePixelSum = []
    patchPixelSum = []
    templateDimR = len(template)
    templateDimC = len(template[0])
    patchDimR = len(patch)
    patchDimC = len(patch[0])

    for i in range (templateDimR):
        templatePixelSum.append(sum(template[i]))
    templateMean = sum(templatePixelSum)/(templateDimR*templateDimC)

    for i in range (patchDimR):
        patchPixelSum.append(sum(patch[i]))
    patchMean = sum(patchPixelSum)/(patchDimR*patchDimC)

    numeratorSum = 0
    templateVarianceSum = 0
    patchVarianceSum = 0

    # print(templateDimR, templateDimC, patchDimR, patchDimC)

    for i in range(templateDimR):
        for j in range(templateDimC):
            # print('i, j', i, j)
            numeratorSum += ((template[i][j]-templateMean)*(patch[i][j]-patchMean))
            templateVarianceSum += (template[i][j]-templateMean)**2
            patchVarianceSum += (patch[i][j]-patchMean)**2
    # templateVariance = templateVarianceSum**0.5
    # patchVariance = patchVarianceSum**0.5
    denominator = (templateVarianceSum*patchVarianceSum)**0.5

    ncc = numeratorSum/denominator

    return ncc



def match(img, template):
    """Locates the template, i.e., a image patch, in a large image using template matching techniques, i.e., NCC.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        x (int): row that the character appears (starts from 0).
        y (int): column that the character appears (starts from 0).
        max_value (float): maximum NCC value.
    """
    # TODO: implement this function.
    # raise NotImplementedError
    # raise NotImplementedError
    maxNCC = -1
    templateDimR = len(template)
    templateDimC = len(template[0])
    imgDimR = len(img)
    imgDimC = len(img[0])
    # paddedImg = utils.zero_pad(img, templateDimR-1, templateDimC-1)

    # print(templateDimR, templateDimC, len(paddedImg), len(paddedImg[0]))


    for i in range(0, imgDimR-templateDimR-1):
        for j in range(0, imgDimC-templateDimC-1):
            # patch = utils.crop(paddedImg, i, i+templateDimR, j, j+templateDimC)
            patch = utils.crop(img, i, i+templateDimR, j, j+templateDimC)
            ncc = norm_xcorr2d(patch, template)
            if(ncc > maxNCC):
                maxNCC = ncc
                locationX = i
                locationY = j
    return locationX, locationY, maxNCC


def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()

    img = read_image(args.img_path)
    # template = utils.crop(img, xmin=10, xmax=30, ymin=10, ymax=30)
    # template = np.asarray(template, dtype=np.uint8)
    # cv2.imwrite("./data/proj1-task2-template.jpg", template)
    template = read_image(args.template_path)

    x, y, max_value = match(img, template)
    # The correct results are: x: 17, y: 129, max_value: 0.994
    with open(args.rs_path, "w") as file:
        json.dump({"x": x, "y": y, "value": max_value}, file)


if __name__ == "__main__":
    main()
