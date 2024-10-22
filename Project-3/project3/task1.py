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
    unique = np.unique(img)
    centroids.append(np.random.choice(unique))
    centroids.append(np.random.choice(unique))
    dist = 9999999
    min_dist = 9999999
    sum_min_dist = 0
    cluster_labels = list()
    labels = list()
    distances = list()
    old_centroids = list()
    j = 0
    length = 0
    init_centers = list()
    final_distance = 999999999
    final_centroids = list()
    final_labels = list()
    final_dist = 9999999999999
    
    pixel_dict={}
    for i in img:
        for j in i:
            if j in pixel_dict:
                pixel_dict.__setitem__(j,pixel_dict.get(j)+1)
            else:
                pixel_dict.__setitem__(j,1)

    for i in range(len(unique)):
            while(j!=len(unique)):
                if(i!=j):
                    init_centers.append([unique[i],unique[j]])
                j=j+1
            j=i+1
    # k = 0
    for init_center in init_centers:
        # k += 1
        centroids[0] = init_center[0]
        centroids[1] = init_center[1]
        while(centroids!=old_centroids):
            cluster_labels = np.copy(img)
            old_centroids = centroids[:]
            for keys in pixel_dict:
                distance_1 = abs(centroids[0] - keys)
                distance_2 = abs(centroids[1] - keys)
                if(distance_1<distance_2):
                    min_dist = distance_1*pixel_dict.get(keys)
                    label = 0
                else:
                    min_dist = distance_2*pixel_dict.get(keys)
                    label = 1
                cluster_labels[cluster_labels==keys] = label
                sum_min_dist += min_dist
                dist = 9999999
                min_dist = 9999999
            final_distance = sum_min_dist
            sum_min_dist = 0
            labels = np.reshape(cluster_labels,(img.shape[0],img.shape[1]))
            cluster_labels = list()
            centroids[0]=np.mean(np.ma.array(img,mask=(labels)))
            centroids[1]=np.mean(np.ma.array(img,mask=np.logical_not(labels)))
        if(final_distance<final_dist):
            final_centroids = centroids
            final_labels = labels
            final_dist = final_distance
    return(final_centroids,final_labels, final_dist)
        
    # return final_centroids,final_labels, final_dist 


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
    
    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')