import math
import sys
import os
import module_1
import module_2
import module_3
import numpy
import uuid

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


def create_document_term_matrix_2(labels, order, images_ids, k):
    dt_matrix = []
    for ids in images_ids:
        vector = [0 for i in range(k)]
        for i, id_order in enumerate(order):
            if str(ids[0]) == str(id_order):
                vector[labels[i]] += 1
        dt_matrix.append(vector)

    return dt_matrix, [file[1] for file in images_ids]


def runkmeans(parameters_file, output_to_file):
    parameters_file = open(parameters_file, 'r')
    parameters_file_contents = parameters_file.readlines()

    imgs_dir = parameters_file_contents[0].strip()
    k = int(parameters_file_contents[1].strip())

    entities_text = []
    images_ids = []
    for file in os.listdir(imgs_dir):
        if file == "parameters.txt":
            continue

        boxes = module_1.run(imgs_dir + file, "", False)
        text = module_2.get_all_text_from_image(imgs_dir + file, boxes)
        processed_text = module_3.process_text(text)

        id = uuid.uuid4()
        images_ids.append([id, file])

        for object in processed_text:
            if object[0] == "entity" or object[0] == "weakentity":
                entities_text.append(
                    [id, object[1]["Title"] + " " + object[1]["Text"]])
    dt_matrix, order = create_document_term_matrix(entities_text)

    # First clustering of all entities
    prev_score = -sys.maxsize - 1
    k_initial = 0
    for i in range(3, 10):
        kmean = KMeans(n_clusters=i)
        kmean.fit(numpy.array(dt_matrix[1:]))
        label = kmean.predict(dt_matrix[1:])
        score = silhouette_score(dt_matrix[1:], label)
        if score > prev_score:
            prev_score = score
            k_initial = i

    kmean = KMeans(n_clusters=k_initial)
    kmean.fit(numpy.array(dt_matrix[1:]))

    # Second clustering of ERD images
    dt_matrix_2, order_2 = create_document_term_matrix_2(
        kmean.labels_, order, images_ids, k_initial)

    if k == 0:
        prev_score = -sys.maxsize - 1
        for i in range(2, len(dt_matrix_2) - 1):
            kmean = KMeans(n_clusters=i)
            kmean.fit(numpy.array(dt_matrix_2))
            label = kmean.predict(dt_matrix_2)
            score = silhouette_score(dt_matrix_2, label)
            if score > prev_score:
                prev_score = score
                k = i

    kmean = KMeans(n_clusters=k)
    kmean.fit(numpy.array(dt_matrix_2))

    output = [[] for i in range(k)]

    for i, cluster in enumerate(kmean.labels_):
        output[cluster].append(order_2[i])

    if output_to_file:
        print("Clustering is outputed to advanced_clusters.txt where k=" + str(k))

        with open("advanced_clusters.txt", "w") as output_file:
            for files in output:
                output_file.write(" ".join(files) + "\n")

    return kmean.labels_
