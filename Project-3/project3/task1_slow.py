import utils
import numpy as np
import json
import time


def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    # TODO: implement this function.
    np.random.seed(42)
    centroids = list()
    cluster_label = list()
    cluster_labels = list()
    distances = list()
    old_centroids = list()
    dist = 0
    min_dist = 2147483646
    sum_min_dist = 0
    final_distance = 2147483645
    final_dist = 2147483646
    final_centroids = list()
    final_cluster_labels = list()
    unique = np.unique(img)
    centroids.append(np.random.choice(unique))
    centroids.append(np.random.choice(unique))
    j = 0
    length = 0
    init_centers = list()
    for i in range(len(unique)):
        while(j!=len(unique)):
            if(i!=j):
                init_centers.append([unique[i],unique[j]])
            j = j+1
        j = i+1

    for init_center in init_centers:
        centroids[0] = init_center[0]
        centroids[1] = init_center[1]
        while(centroids!=old_centroids):
            old_centroids = centroids[:]
            for i in img:
                for j in i:
                    for center in centroids:
                        dist = np.sqrt((center - j)**2)
                        if(dist<min_dist):
                            min_dist = dist
                            if(center==centroids[1]):
                                label = 1
                            else:
                                label = 0
                        elif(dist == min_dist):
                            min_dist = dist
                            if(centroids[1]<centroids[0]):
                                label = 1
                            else:
                                label = 0
                    cluster_label.append(label)
                    sum_min_dist += min_dist
                    dist = 0
                    min_dist = 2147483646
            final_distance = sum_min_dist
            sum_min_dist = 0
            cluster_labels = np.reshape(cluster_label,(img.shape[0],img.shape[1]))
            cluster_label.clear()
            centroids[0] = np.mean(np.ma.array(img, mask=(cluster_labels)))
            centroids[1] = np.mean(np.ma.array(img, mask=np.logical_not(cluster_labels)))
        if(final_distance<final_dist):
            for i in range(len(centroids)):
                centroids[i] = int(round(centroids[i]))
            final_centroids = centroids
            final_cluster_labels = cluster_labels
            final_dist = final_distance

    return final_centroids, final_cluster_labels, final_dist 


def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    # TODO: implement this function.

    x = np.empty(shape=(img.shape[0],img.shape[1]))

    x[labels==0] = centers[0]
    x[labels==1] = centers[1]

    return x.astype(np.uint8)


if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')