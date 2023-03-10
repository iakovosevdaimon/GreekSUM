"""
Modified version of
https://github.com/Tixierae/OrangeSum/blob/main/compute_overlap.py

# Original copyright is appended below.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""

import re
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')
import os
import json
import string
from nltk import ngrams
import argparse


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
parser = argparse.ArgumentParser()
parser.add_argument('--path_predictions', '-pred', default=None, type=str, help='Path to predictions\' file')
parser.add_argument('--path_article', '-art', default=None, type=str, help='Path to artile')
#parser.add_argument('--dataset_type','-dt', default=None, type=str, help='The type of GreekSum dataset. Accepted values are: Abstract or Title')

nmax = 4 # greatest n-gram order to consider
min_size = 20

args = parser.parse_args()

#path_pred = './title/generated_output.txt'
#path_ref = './title/summarization_data_title/test-article.txt'
path_pred = args.path_predictions
path_art = args.path_article


lens = []

results = dict()
counter = 0

with open(path_pred, 'r') as fr1, open(path_art, 'r') as fr2:
    for line1, line2 in zip(fr1, fr2):
        article = line2.strip()
        head = line1.strip()
        lens.append(len(head.split()))
        if len(article.split()) > min_size:

            to_save = dict()
            # whenever the field is too short to have at least one nmax-gram, NA is returned
            to_save['pred'] = pct_novel_ngrams_in_y(article,head,nmax)

            results[counter]=to_save
            counter+=1

print('= = = size (in nb of words) of predictions = = =')
print('min: %s, max: %s, average: %s, median: %s' % (min(lens),max(lens),round(np.mean(lens),2),np.median(lens)))


print('= = = = percentage of novel ngrams in: predictions = = = =')
for n in range(1,nmax + 1):
    print('* * * * order:',n,'* * * *')
    print(round(np.mean([v['pred'][int(n)] for k,v in results.items() if not v['pred'][int(n)] == 'NA']),1))
