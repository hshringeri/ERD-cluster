import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
ps = PorterStemmer()

def process_text(texts):
    for i in range(len(texts)):
        texts[i][1] = texts[i][1].replace("_", " ")
        texts[i][1] = texts[i][1].replace("-", " ")
        text_tokens = word_tokenize(texts[i][1])
        tokens_without_sw = [ps.stem(word) for word in text_tokens if not word in stopwords.words() and not word == "PK"]

        texts[i][1] = " ".join(tokens_without_sw)
        texts[i][1] = re.sub(r"\s[A-Za-z]\s", " ", texts[i][1])
    return texts
