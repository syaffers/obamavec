import logging
from gensim.models import KeyedVectors

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
obama_vec = KeyedVectors.load_word2vec_format("obama_vec.bin", binary=True)

print("Testing model...")
obama_vec.accuracy('/home/syafiq/data/questions-words.txt')
