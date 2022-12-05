import math
import sys
import os
import module_1
import module_2
import module_3
import random

def euclideanDistance(x, y):
    S = 0
    for i in range(len(x)):
        S += math.pow(x[i]-y[i], 2)

    return math.sqrt(S)


def updateMean(n, mean, item):
    for i in range(len(mean)):
        m = mean[i]
        m = (m*(n-1)+item[i])/float(n)
        mean[i] = round(m, 3)

    return mean


def classify(means, item):
    minimum = sys.maxsize
    index = -1

    for i in range(len(means)):
        dis = euclideanDistance(item, means[i])

        if (dis < minimum):
            minimum = dis
            index = i

    return index


def calculateMeans(items, means, maxIterations=100000):
    clusterSizes = [0 for i in range(len(means))]

    # Specify the cluster each document belongs to
    belongsTo = [0 for i in range(len(items))]

    print("Calculating k-means++...")
    for e in range(maxIterations):
        noChange = True
        for i in range(len(items)):
            item = items[i]

            # Find out which cluster the document belongs to
            index = classify(means, item)

            clusterSizes[index] += 1
            cSize = clusterSizes[index]

            # Recalculate cluster centroid
            means[index] = updateMean(cSize, means[index], item)

            if (index != belongsTo[i]):
                noChange = False

            belongsTo[i] = index

        if (noChange):
            break

    return means, belongsTo


def create_document_term_matrix(docs_text):
    all_text = ""
    for doc in docs_text:
        all_text += doc[1] + " "
    unique_words = list(set(all_text.split()))

    dt_matrix = []
    dt_matrix.append(unique_words)

    for doc in docs_text:
        vector = [0 for i in range(len(unique_words))]

        for i, word in enumerate(unique_words):
            if i == 0: continue
            vector[i] = 0 if doc[1].count(word) == 0 else math.log(doc[1].count(word)) + 1
        dt_matrix.append(vector)

    return dt_matrix, [doc[0] for doc in docs_text]


def create_bag_of_words(text):
    bag_of_words = ""
    for object in text:
        bag_of_words += object[1] + " "
    
    return bag_of_words.strip()


def runkmeans(parameters_file):
    parameters_file = open(parameters_file, 'r')
    parameters_file_contents = parameters_file.readlines()

    imgs_dir = parameters_file_contents[0].strip()
    k = int(parameters_file_contents[1].strip())

    docs_text = []

    for file in os.listdir(imgs_dir):
        if file == "parameters.txt":
            continue

        boxes = module_1.run(imgs_dir + file, "", False)
        text = module_2.get_all_text_from_image(imgs_dir + file, boxes)
        bag_of_words = create_bag_of_words(text)
        docs_text.append([file, bag_of_words])

    dt_matrix, order = create_document_term_matrix(docs_text)

    centroids = random.choices(dt_matrix[1:], k=k)
    means, belongsTo = calculateMeans(dt_matrix[1:], centroids)
    
    output = [[] for i in range(k)]

    for i, cluster in enumerate(belongsTo):
        output[cluster].append(order[i])
    
    with open("base_line_clusters.txt", "w") as output_file:
        for files in output:
            output_file.write(" ".join(files) + "\n")