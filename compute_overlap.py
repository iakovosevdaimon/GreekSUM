"""
Modified version of
https://github.com/Tixierae/OrangeSum/blob/main/compute_overlap.py

# Original copyright is appended below.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""


import os
import json
import string
from nltk import ngrams


def pct_novel_ngrams_in_y(x,y,nmax):

    # remove punctuation and lowercase
    x = x.translate(str.maketrans('', '', string.punctuation)).lower()
    y = y.translate(str.maketrans('', '', string.punctuation)).lower()

    percs = dict()
    for n in range(1,nmax+1):
        ngrams_x = set(ngrams(x.split(),n))
        ngrams_y = set(ngrams(y.split(),n))
        if len(ngrams_y) == 0:
            percs[n] = 'NA'
        else:
            percs[n] = round(100*len(ngrams_y.difference(ngrams_x))/len(ngrams_y),1)

    return percs

# = = = = =

nmax = 4 # greatest n-gram order to consider
min_size = 20

overlap_path = "./data/overlap"
if not os.path.isdir(overlap_path):
    os.mkdir(overlap_path)

path_to_docs = './data/sum_data/parsed/'

docnames = os.listdir(path_to_docs)

results = dict()

print('Total documents: '+str(len(docnames)))

for counter,docname in enumerate(docnames):

    with open(path_to_docs + docname, 'r', encoding='utf8') as file:
        doc = json.load(file)

    article = doc['article']
    title = doc['title']
    heading = doc['abstract']

    # empty (or too short) articles won't have an entry in 'results'
    if len(article.split()) > min_size:

        to_save = dict()
        # whenever the field is too short to have at least one nmax-gram, NA is returned
        to_save['t'] = pct_novel_ngrams_in_y(article,title,nmax)
        to_save['h'] = pct_novel_ngrams_in_y(article,heading,nmax)
        to_save['t+h'] = pct_novel_ngrams_in_y(article,title + ' ' + heading,nmax)

        results[docname] = to_save

    if counter % round(len(docnames)/10) == 0:
        print(counter)

print(len(docnames) - len(results), 'too short documents')

with open('./data/overlap/overlaps.json', 'w', encoding='utf8') as file:
    json.dump(results, file, sort_keys=True, indent=4, ensure_ascii=False)
