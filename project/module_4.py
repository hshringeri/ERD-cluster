import math
import sys
import os
import module_1
import module_2
import module_3
import random
import numpy
import copy


def updateCentroids(belongsTo, items, k):
    clusters = [[] for i in range(k)]

    for i in range(len(belongsTo)):
        clusters[belongsTo[i]].append(items[i])

    new_centroids = [numpy.mean(numpy.array(cluster), axis=0).tolist() if len(
        cluster) > 0 else random.choice(items) for cluster in clusters]

    return new_centroids


def classify(centroids, item):
    minimum = sys.maxsize
    index = -1

    for i in range(len(centroids)):
        dis = math.dist(item, centroids[i])

        if (dis < minimum):
            minimum = dis
            index = i

    return index


def calculateMeans(items, centroids, maxIterations=100000):
    belongsTo = [-1 for i in range(len(items))]
    iterations = 0
    old_centroids = None

    print("Calculating clusters using k-means++...")

    while not should_stop(old_centroids, centroids, iterations, maxIterations):
        iterations += 1
        old_centroids = copy.deepcopy(centroids)

        for i in range(len(items)):
            belongsTo[i] = classify(centroids, items[i])

        centroids = updateCentroids(belongsTo, items, len(centroids))

    return centroids, belongsTo


def should_stop(old_centroids, centroids, iterations, maxIterations):
    if iterations > maxIterations:
        return True
    if old_centroids == None:
        return False

    for i in range(len(old_centroids)):
        for j in range(len(old_centroids[i])):
            if not math.isclose(old_centroids[i][j], centroids[i][j]):
                return False
    return True


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
            if i == 0:
                continue
            vector[i] = 0 if doc[1].count(
                word) == 0 else math.log(doc[1].count(word)) + 1
        dt_matrix.append(vector)

    return dt_matrix, [doc[0] for doc in docs_text]


def create_bag_of_words(text):
    bag_of_words = ""
    for object in text:
        if object[0] == "entity" or object[0] == "weakentity":
            bag_of_words += object[1]["Title"] + " "
            bag_of_words += object[1]["Text"] + " "
        else:
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
        processed_text = module_3.process_text(text)
        bag_of_words = create_bag_of_words(processed_text)
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
