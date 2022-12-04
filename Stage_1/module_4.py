import module_3
import gensim
from gensim import corpora
from gensim.utils import simple_preprocess
import math
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

test = [[['attribute', 'start_date'], ['attribute', 'starting_mileage'], ['attribute', 'end_date'], ['relationship', 'Rents'], ['relationship', 'Owns'], ['weakrelationship', 'Recalled'], ['weakrelationship', 'For'], ['weakrelationship', 'Writes'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Pays'], ['entity', 'Customer', 'customerid', 'name', 'credit_card_no'], ['entity', 'Car', 'PKVIN_no', 'make', 'model', 'year', 'current_mileage'], ['weakentity', 'Review', 'date', 'time', 'description', 'num_of_stars'], ['entity', 'Driver', 'licenseno', 'state', 'name', 'age'], ['weakentity', 'Recall', 'date', 'description'], ['weakentity', 'Rent_Installment', 'date', 'amount']],
[['attribute', 'start_date'], ['attribute', 'starting_mileage'], ['attribute', 'end_date'], ['relationship', 'Rents'], ['relationship', 'Owns'], ['weakrelationship', 'Recalled'], ['weakrelationship', 'For'], ['weakrelationship', 'Writes'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Pays'], ['entity', 'Customer', 'customerid', 'name', 'credit_card_no'], ['entity', 'Car', 'PKVIN_no', 'make', 'model', 'year', 'current_mileage'], ['weakentity', 'Review', 'date', 'time', 'description', 'num_of_stars'], ['entity', 'Driver', 'licenseno', 'state', 'name', 'age'], ['weakentity', 'Recall', 'date', 'description'], ['weakentity', 'Rent_Installment', 'date', 'amount']]]

#Returns a list of dictionarys with the key as the term number and the value
#  as the term frequecny, using log(tf)+1 , and an example input given above
#  if a key is not found, its value is 0
def term_feq_matrix(erd_list):
    tfm = []
    dictionary = corpora.Dictionary()
    BOW_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in erd_list]
    for x in range(0, len(BOW_corpus)):
        doc = {}
        for y in range(0, len(BOW_corpus[x])):
            if BOW_corpus[x][y][1] >= 1:
                doc.update({BOW_corpus[x][y][0] : (math.log(BOW_corpus[x][y][1]))+1})
            else:
                doc.update({BOW_corpus[x][y][0] : BOW_corpus[x][y][1]})
        tfm.append(doc)
    return tfm

def kmeans_plusplus(n_clusters, tfm):
    kmeans = KMeans(n_clusters=n_clusters).fit(tfm)
    return kmeans

#Takes the term frequency matrix return from
# term_feq_matrix(erd_list) and converts it from
# a list of dictionarys ([{},{}], where each dictionary
# is the tfm for each diagram) and turns it into a list
# of lists ([[],[]]) of eqaul sizes
def tfm_cleanup(tfm):
    doc = []
    keys = []
    for x in tfm:
        for y in x.keys():
            if y not in keys:
                keys.append(y)
    for x in range(0, len(tfm)):
        t = []
        for k in keys:
            t.append(tfm[x].get(k, 0))
        doc.append(t)
    return doc

def silhouette_score():
    #TODO
    return k_clusters


print(kmeans_plusplus(2, tfm_cleanup(term_feq_matrix(module_3.stem(test)))))