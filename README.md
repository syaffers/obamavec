# ObamaVec, word embeddings of Barack Obama's speeches

## Quick start

Download the pre-trained `gensim` model [here](https://s3.amazonaws.com/syaffers-stuff/obama-vec/obama_vec.bin) (3.9MB).

Install `gensim` (if you haven't already):

    pip install gensim

Play with the model:

    python -i load_obama_vec.py

    >>> obama_vec.most_similar(positive=["president", "woman"], negative=["man"] )
    [('trump', 0.708624541759491),
     ('hillary', 0.703040361404419),
     ('presidentelect', 0.6651997566223145),
     ('barack', 0.6554529666900635),
     ('nominee', 0.6548861861228943),
     ('snowden', 0.6519112586975098),
     ('governor', 0.649947464466095),
     ('putins', 0.6497337818145752),
     ('senator', 0.6418864727020264),
     ('putin', 0.6408566832542419)]



## Build your own

The raw data can be found [here](https://s3.amazonaws.com/syaffers-stuff/obama-vec/raw_speeches.tar.gz) (3.1MB). Alternatively, you could scrape the data yourself:

    make scrape

Then, you can edit the `make_obama_vec.py` file to your liking. You will need `nltk` and `gensim` to be installed for the next step. To compile your model simply:

    make vector

This will perform cleaning on the raw data and place it into the `processed/` folder.

For more information on cleaning, consult `clean_raw_files.sh`. Essentially it's removing some unwanted artifacts from the raw data and removing "Speaker tags" which is when the data has something like

> President Obama: ... thank you. Question: What do you...

The script removes the "President Obama:" and "Question:" parts leaving just the discourse.


## Description

### Data Source

This simple word embedding exercise came up while I sat in a long speech and wondered if I could mine leaders speeches and do some analysis. Nothing politically-oriented either, just... fun.

So it turns out that [this guy](http://www.americanrhetoric.com/) has an American presidents speech bank which is perfect. Upon more inspection, there is a section specifically for all the speeches by Barack Obama. In total, there were 435 speeches of varying length and content which seemed to be good for a hobby scale project.

The mining was slightly cumbersome: the site didn't use good HTML practices which made it difficult but I did my best by eyballing certain parts of the documents which act as markers where I can snip off without too much unnecessary residue.

Cleaning was another huge part. Lots of different "Speaker tags" for the same people and it became quite laborious. No stemming was done, nor of conversion of numbers into words (17 to seventeen). After all this and splitting the words, it ended up being around 4,000,000 words in total.

### Model

The uploaded model is trained using `gensim` with the following parameters:

* 100 features
* At least 30 words appearing in the corpus
* Context window length: 4

There are 10005 words in the vocab, mostly tied to political themes (as you might imagine). Surprisingly, it does pretty well with the family predictions. In the end, this model is by no means "good". In fact, it's far from it :joy:. Here's a table of results on various parameters:

| Features | Window | `questions-words.txt` accuracy |
| -------- |:------:|:------------------------------:|
| 50       | 4      | 7.2%                           |
| 50       | 5      | 6.3%                           |
| 50       | 6      | 5.9%                           |
| 50       | 7      | 6.4%                           |
| 50       | 8      | 5.8%                           |
| 100      | 4      | 7.5%                           |
| 100      | 5      | 7.0%                           |
| 100      | 6      | 7.0%                           |
| 100      | 7      | 6.7%                           |
| 100      | 8      | 7.0%                           |
| 150      | 4      | 7.4%                           |
| 150      | 5      | 6.7%                           |
| 150      | 6      | 6.9%                           |
| 150      | 7      | 6.4%                           |
| 150      | 8      | 6.5%                           |
