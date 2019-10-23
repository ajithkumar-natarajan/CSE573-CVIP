"""
RANSAC Algorithm Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to fit a line to the given points using RANSAC algorithm, and output
the names of inlier points and outlier points for the line.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
You can use the library random
Hint: It is recommended to record the two initial points each time, such that you will Not 
start from this two points in next iteration.
"""
import random
from itertools import permutations



def calculate_perpendicular_dist(a, b, c):
    return (abs(((b[1] - a[1]) * c[0]) - ((b[0] - a[0]) * c[1]) + (b[0] * a[1]) - (b[1] * a[0])) / (((b[1] - a[1])**2 + (b[0] - a[0])**2)**(1/2)))


def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
           (more information can be found on the page 90 of slides "Image Features and Matching")
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    # TODO: implement this function.
    # raise NotImplementedError
    selected_points = set()
    points = list()

    for point in input_points:
        points.append(list((point.values()))[1])
    no_of_points = len(points)
    output = list()
    iterations = len(list(permutations(range(0, no_of_points),2)))

    for itr in range(iterations):
        sample = random.sample(range(0, no_of_points), 2)
        while(tuple(sample) in selected_points):
            sample = random.sample(range(0, no_of_points), 2)

        selected_points.add(tuple(sample))

        count = 0
        avg_dist = 0.00
        for i in range(no_of_points):

            if(i == sample[0] or i == sample[1]):
                pass
            else:
                dist = calculate_perpendicular_dist(points[sample[0]], points[sample[1]], points[i])
                if(dist <= t):
                    count += 1
                    avg_dist += dist
        if(count >= d):
            avg_dist = avg_dist/count

            result = dict()
            result['key'] = sample
            result['value'] = avg_dist
            result['count'] = count
            output.append(result)
    sorted_output = sorted(output, key=lambda v: v['value'])

    output_to_file_1 = list()
    output_to_file_2 = list()
    result_key = sorted_output[0]

    sample = result_key['key']
    for i in range(no_of_points):
        if(i == sample[0] or i == sample[1]):
            output_to_file_1.append(chr(i+97))
        else:
            dist = calculate_perpendicular_dist(points[sample[0]], points[sample[1]], points[i])
            if(dist <= t):
                output_to_file_1.append(chr(i+97))
            else:
                output_to_file_2.append(chr(i+97))
    return output_to_file_1, output_to_file_2




if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    assert len(inlier_points_name) + len(outlier_points_name) == 8
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()
