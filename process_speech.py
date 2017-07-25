import re
import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from scipy.spatial.distance import pdist, squareform

"""
speech364
speech423
speech290
speech80 -> add President
"""


def truncate_qna(text):
    """Remove the Q&A parts of a speech leaving Barack's speeches only"""
    if "Question:" in text:
        return text.split("Question:")[0]

    if "Questions?" in text:
        return text.split("Questions?")[0]

    if "Q:" in text:
        return text.split("Q:")[0]

    return text


def clean_start(text):
    """Clear any starting texts which is not part of the actual speech"""
    return text.replace("click for flash", "")\
               .replace("[Introductory remarks]", "")\
               .replace("as prepared for delivery", "")\
               .replace("AUTHENTICITY CERTIFIED", "")


def remove_specialchars(text):
    """Remove unwanted special characters"""
    return re.sub(r"[^A-Za-z0-9\s]", "", text)


def remove_xa0(text):
    """Remove weird hex texts"""
    return text.replace("\xa0", " ")


def flatten_number(text):
    """Change some number in text to NUMBER"""
    return re.sub(r"(\d+|\d{1,3}(,\d{3})*)(\.\d+)?", "NUMBER", text)

d = {}
stemmer = LancasterStemmer()
sw = stopwords.words("english")
words_dict = {}
num_files = 50

X = []
for filename in glob.glob("raw/*")[:num_files]:
    with open(filename, encoding='utf-8') as f:
        data = f.read().splitlines()[0]
        data = truncate_qna(data).strip()
        # data = remove_specialchars(data).strip()
        data = flatten_number(data).strip()
        data = remove_xa0(data).strip()
        data = clean_start(data).strip()
        data = data.replace("  ", " ")
        data = data.replace("   ", " ")
        data = data.replace("    ", " ")

    words = nltk.word_tokenize(data)
    stems = list(set([stemmer.stem(w) if w not in sw else "" for w in words]))

    for stem in stems:
        if stem in words_dict:
            words_dict[stem] += 1
        else:
            words_dict[stem] = 1

# clearing unnecessary punctuation
del words_dict['']
del words_dict["''"]
del words_dict['``']
del words_dict[':']
del words_dict[';']
del words_dict['--']
del words_dict[',']
del words_dict[']']
del words_dict["'"]
del words_dict["?"]
del words_dict["."]

ref = np.array(list(words_dict.keys()))
X = np.array(list(words_dict.values()))

# generate feature vectors
ref_features = ref[X > int(num_files / 2)]
features = X[X > int(num_files / 2)]

print("Done generating features...")
docs = []

for filename in glob.glob("raw/*")[:num_files]:
    bag = np.zeros(len(features))
    with open(filename, encoding='utf-8') as f:
        data = f.read().splitlines()[0]
        data = truncate_qna(data).strip()
        # data = remove_specialchars(data).strip()
        data = flatten_number(data).strip()
        data = remove_xa0(data).strip()
        data = clean_start(data).strip()
        data = data.replace("  ", " ")
        data = data.replace("   ", " ")
        data = data.replace("    ", " ")

    words = nltk.word_tokenize(data)
    stems = [stemmer.stem(w) if w not in sw else "" for w in words]

    for stem in stems:
        if stem in ref_features:
            bag[np.where(ref_features == stem)[0][0]] += 1
    
    docs.append(bag)

docs = np.array(docs)

pca = PCA(n_components=2)
X_t = pca.fit_transform(scale(docs))
plt.scatter(X_t[:, 0], X_t[:, 1])
plt.show()
Y = pdist(docs, 'euclidean')
Z = squareform(Y)
# sns.clustermap(Z)
# plt.show()
