"""
Calculate some statistics of the GreekSUM Title/Abstract dataset
"""



import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize
import argparse
import nltk
nltk.download('punkt')

parser = argparse.ArgumentParser()

parser.add_argument('--dataset_name', '-d_name', default=None, type=str, help="Name of GreekSum dataset. Possible values are:'title' or 'abstract' or 'all'(all option refers to the dataset before being splitted into Abstract or Title)")

args = parser.parse_args()

path_to_docs = './data/sum_data/parsed/'

files = []
if args.dataset_name.lower() == "title":
    fr = open("./splits_title_as_summary/train.txt","r")
    for line in fr:
        files.append(line.strip())
    fr.close()
    fr = open("./splits_title_as_summary/valid.txt","r")
    for line in fr:
        files.append(line.strip())
    fr.close()
    fr = open("./splits_title_as_summary/test.txt","r")
    for line in fr:
        files.append(line.strip())
    fr.close()
    print('GreekSum Title contains '+str(len(files))+' articles')
elif args.dataset_name.lower() == "abstract":
    fr = open("./splits_abstract_as_summary/train.txt","r")
    for line in fr:
        files.append(line.strip())
    fr.close()
    fr = open("./splits_abstract_as_summary/valid.txt","r")
    for line in fr:
        files.append(line.strip())
    fr.close()
    fr = open("./splits_abstract_as_summary/test.txt","r")
    for line in fr:
        files.append(line.strip())
    fr.close()
    print('GreekSum Abstract contains '+str(len(files))+' articles')
else:
    files = os.listdir(path_to_docs)
    print('GreekSum contains '+str(len(files))+' articles')


#docnames = os.listdir(path_to_docs)

my_keys = ['title','abstract','article']
lens = dict(zip(my_keys,[[],[],[]]))

sent_lens = dict(zip(my_keys,[[],[],[]]))

nmax = 4 # greatest n-gram order considered in 'compute_overlap.py'

for counter,docname in enumerate(files):

    with open(path_to_docs + docname, 'r', encoding='utf8') as file:
        doc = json.load(file)

    for key in my_keys:
        sent_lens[key].append(len(sent_tokenize(doc[key].strip())))
        lens[key].append(len(doc[key].split()))

    if counter % round(len(files)/10) == 0:
        print(counter)

for key in my_keys:

    print('= = = size (in nb of sentences) of',key,'= = =')
    print('min: %s, max: %s, average: %s, median: %s' % (min(sent_lens[key]),max(sent_lens[key]),round(np.mean(sent_lens[key]),2),np.median(sent_lens[key])))

    print('= = = size (in nb of words) of',key,'= = =')
    print('min: %s, max: %s, average: %s, median: %s' % (min(lens[key]),max(lens[key]),round(np.mean(lens[key]),2),np.median(lens[key])))

    print('nb of docs with empty',key,':',len([elt for elt in lens[key] if elt == 0]))

    print('nb of docs with <= 5 words',key,':',len([elt for elt in lens[key] if elt <= 5]))

    if key == 'article':
        print('nb of docs with article <= 20 words:',len([elt for elt in lens[key] if elt <= 20]))

    plt.figure()
    plt.hist(lens[key],density=False)
    plt.grid(True)
    plt.xlabel('Nb of words')
    plt.ylabel('Counts')
    plt.title('Size (in nb of words) of ' + key)
    plt.savefig('./data/plots/' + 'size_distr_' + key + '.pdf')

with open('./data/overlap/overlaps.json', 'r', encoding='utf8') as file:
    overlaps = json.load(file)

for key in ['t','h','t+h']:

    print('= = = = percentage of novel ngrams in:',key,'= = = =')

    for n in range(1,nmax + 1):
        print('* * * * order:',n,'* * * *')
        print(round(np.mean([v[key][str(n)] for k,v in overlaps.items() if not v[key][str(n)] == 'NA' and k in files]),1))

for perc in [10,20,30,40,50,60]:
    print('= = = = nb of title+abstract summaries with at least:',perc,'% new unigrams = = = =')
    print(len([k for k,v in overlaps.items() if v['t+h']['1'] >= perc]))
