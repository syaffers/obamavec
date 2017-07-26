import re
import glob
import nltk
import logging
from gensim.models import KeyedVectors
from gensim.models import Word2Vec, word2vec, phrases
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords


def remove_specialchars(text):
    """Remove unwanted special characters"""
    out = re.sub("--", " ", text)
    out = re.sub(r"\.\.\.", " ", out)
    return out


def remove_xa0(text):
    """Remove weird hex texts"""
    return text.replace("\xa0", " ")


def sentence_to_wordlist(sentence, remove_stopwords=False):
    """Converts sentence to list of words"""
    sentence_text = re.sub(r'[^\w\s]', '', sentence)
    words = sentence_text.lower().split()
    return words


def speech_to_sentences(speech, tokenizer):
    """Converts speech to arrays of arrays of words"""
    raw_sentences = tokenizer.tokenize(speech)
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(sentence_to_wordlist(raw_sentence))

    return sentences


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stemmer = LancasterStemmer()
sentences = []
sw = stopwords.words("english")
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
dry_run = True

num_features = 100
min_word_count = 30
num_workers = 4
context = 4
downsampling = 1e-3

if not dry_run:
    for filename in glob.glob("processed/*"):
        with open(filename, encoding='utf-8') as f:
            data = f.read().splitlines()[0]
            data = remove_specialchars(data).strip()
            data = remove_xa0(data).strip()
            # removes multiple whitespaces
            data = " ".join(data.split())

            sentences += speech_to_sentences(data, tokenizer)

        obama_vec = word2vec.Word2Vec(
            sentences, workers=num_workers, size=num_features,
            window=context, sample=downsampling)

        acc = obama_vec.accuracy("/home/syafiq/data/questions-words.txt")
        obama_vec.wv.save_word2vec_format("obama_vec.bin", binary=True)

else:
    obama_vec = KeyedVectors.load_word2vec_format("obama_vec.bin", binary=True)
