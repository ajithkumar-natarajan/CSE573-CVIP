"""
Image Stitching Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.

Do NOT modify the code provided to you.
You are allowed use APIs provided by numpy and opencv, except “cv2.findHomography()” and
APIs that have “stitch”, “Stitch”, “match” or “Match” in their names, e.g., “cv2.BFMatcher()” and
“cv2.Stitcher.create()”.
"""
import cv2
import numpy as np
import random

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """

    ratio = 0.8
    ransac_threshold = 4.0

    descriptor = cv2.xfeatures2d.SIFT_create()

    (keypoints_right_img, features_right_img) = descriptor.detectAndCompute(right_img, None)
    keypoints_right_img = np.float32([keypoint_right_img.pt for keypoint_right_img in keypoints_right_img])

    (keypoints_left_img, features_left_img) = descriptor.detectAndCompute(left_img, None)
    keypoints_left_img = np.float32([keypoint_left_img.pt for keypoint_left_img in keypoints_left_img])

    matcher = cv2.DescriptorMatcher_create("BruteForce")
    raw_matches = matcher.knnMatch(features_right_img, features_left_img, 2)
    matches = list()
    for match in raw_matches:
        if len(match) == 2 and match[0].distance < match[1].distance * ratio:
            matches.append((match[0].trainIdx, match[0].queryIdx))

    if len(matches) > 4:
        points_right_img = np.float32([keypoints_right_img[i] for (_, i) in matches])
        points_left_img = np.float32([keypoints_left_img[i] for (i, _) in matches])

        (homography, mask) = cv2.findHomography(points_right_img, points_left_img, cv2.RANSAC, ransac_threshold)

    # M = (matches, H, status)

    if homography is None:
        return None
    # (matches, H, status) = M

    result = cv2.warpPerspective(right_img, homography, (right_img.shape[1] + right_img.shape[1], right_img.shape[0]))
    result[0:left_img.shape[0], 0:left_img.shape[1]] = left_img

    return result

    raise NotImplementedError

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task2_result.jpg',result_image)


