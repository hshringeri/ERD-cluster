import math
import sys
import os
import module_1
import module_2
import module_3
import random
import numpy
import copy
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


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


def runkmeans(parameters_file, output_to_file):
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

    if k == 0:
        prev_score = -sys.maxsize - 1
        for i in range(2, len(dt_matrix[1:]) - 1):
            kmean = KMeans(n_clusters=i)
            kmean.fit(numpy.array(dt_matrix[1:]))
            label = kmean.predict(dt_matrix[1:])
            score = silhouette_score(dt_matrix[1:], label)
            if score > prev_score:
                prev_score = score
                k = i

    kmean = KMeans(n_clusters=k)
    kmean.fit(numpy.array(dt_matrix[1:]))

    output = [[] for i in range(k)]

    for i, cluster in enumerate(kmean.labels_):
        output[cluster].append(order[i])

    if output_to_file:
        print("Clustering is outputed to base_line_clusters.txt where k=" + str(k))

        with open("base_line_clusters.txt", "w") as output_file:
            for files in output:
                output_file.write(" ".join(files) + "\n")

    return kmean.labels_