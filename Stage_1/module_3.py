from nltk.stem import *
from nltk.tokenize import word_tokenize
stopwords = ['I', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by',
    'com','for', 'from', 'how', 'in', 'is', 'it', 'of', 'on', 'or',
    'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who',
    'will', 'with','the', 'www', '[', ']', '.', ',', '"', ';', ':', '\'']
stemmer = PorterStemmer()
test = [[['attribute', 'start_date'], ['attribute', 'starting_mileage'], ['attribute', 'end_date'], ['relationship', 'Rents'], ['relationship', 'Owns'], ['weakrelationship', 'Recalled'], ['weakrelationship', 'For'], ['weakrelationship', 'Writes'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Pays'], ['entity', 'Customer', 'customerid', 'name', 'credit_card_no'], ['entity', 'Car', 'PKVIN_no', 'make', 'model', 'year', 'current_mileage'], ['weakentity', 'Review', 'date', 'time', 'description', 'num_of_stars'], ['entity', 'Driver', 'licenseno', 'state', 'name', 'age'], ['weakentity', 'Recall', 'date', 'description'], ['weakentity', 'Rent_Installment', 'date', 'amount']],
[['attribute', 'start_date'], ['attribute', 'starting_mileage'], ['attribute', 'end_date'], ['relationship', 'Rents'], ['relationship', 'Owns'], ['weakrelationship', 'Recalled'], ['weakrelationship', 'For'], ['weakrelationship', 'Writes'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Involved'], ['weakrelationship', 'Pays'], ['entity', 'Customer', 'customerid', 'name', 'credit_card_no'], ['entity', 'Car', 'PKVIN_no', 'make', 'model', 'year', 'current_mileage'], ['weakentity', 'Review', 'date', 'time', 'description', 'num_of_stars'], ['entity', 'Driver', 'licenseno', 'state', 'name', 'age'], ['weakentity', 'Recall', 'date', 'description'], ['weakentity', 'Rent_Installment', 'date', 'amount']]]

#removes stop words (list above) and stemms each word.
# Text input above in 'test'
def stem(word_list):
    lists = []
    for x in test:
        a = []
        for y in x:
            for z in y:
                if z not in stopwords:
                    a.append(z)
        lists.append(a)
    return(lists)