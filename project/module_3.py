import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
ps = PorterStemmer()

def process_text(texts):
    for i in range(len(texts)):
        if texts[i][0] == "weakentity" or texts[i][0] == "entity":
            texts[i][1]["Title"] = texts[i][1]["Title"].replace("_", " ")
            texts[i][1]["Title"] = texts[i][1]["Title"].replace("-", " ")
            texts[i][1]["Title"] = texts[i][1]["Title"].replace(",", "")
            texts[i][1]["Title"] = texts[i][1]["Title"].replace(".", "")
            texts[i][1]["Title"] = texts[i][1]["Title"].replace("\"", "")
            texts[i][1]["Title"] = texts[i][1]["Title"].replace("\'", "")

            text_tokens = word_tokenize(texts[i][1]["Title"])
            tokens_without_sw = [ps.stem(word) for word in text_tokens if not word in stopwords.words() and not word == "PK"]

            texts[i][1]["Title"] = " ".join(tokens_without_sw)
            texts[i][1]["Title"] = re.sub(r"\s[A-Za-z]\s", " ", texts[i][1]["Title"])

            texts[i][1]["Text"] = texts[i][1]["Text"].replace("_", " ")
            texts[i][1]["Text"] = texts[i][1]["Text"].replace("-", " ")
            texts[i][1]["Text"] = texts[i][1]["Text"].replace(",", "")
            texts[i][1]["Text"] = texts[i][1]["Text"].replace(".", "")
            texts[i][1]["Text"] = texts[i][1]["Text"].replace("\"", "")
            texts[i][1]["Text"] = texts[i][1]["Text"].replace("\'", "")

            text_tokens = word_tokenize(texts[i][1]["Text"])
            tokens_without_sw = [ps.stem(word) for word in text_tokens if not word in stopwords.words() and not word == "PK"]

            texts[i][1]["Text"] = " ".join(tokens_without_sw)
            texts[i][1]["Text"] = re.sub(r"\s[A-Za-z]\s", " ", texts[i][1]["Text"])
        else:
            texts[i][1] = texts[i][1].replace("_", " ")
            texts[i][1] = texts[i][1].replace("-", " ")
            texts[i][1] = texts[i][1].replace(",", "")
            texts[i][1] = texts[i][1].replace(".", "")
            texts[i][1] = texts[i][1].replace("\"", "")
            texts[i][1] = texts[i][1].replace("\'", "")

            text_tokens = word_tokenize(texts[i][1])
            tokens_without_sw = [ps.stem(word) for word in text_tokens if not word in stopwords.words() and not word == "PK"]

            texts[i][1] = " ".join(tokens_without_sw)
            texts[i][1] = re.sub(r"\s[A-Za-z]\s", " ", texts[i][1])
    return texts
