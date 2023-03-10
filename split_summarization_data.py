#split jsons to abstract generation task and to title generation task
#split to train(source, target), train(source, target) and train(source, target)
"""
Modified version of
https://github.com/Tixierae/OrangeSum/blob/main/filter_split.py

# Original copyright is appended below.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""
"""
we remove all empty articles, and articles whose
titles were shorter than 5 words
"""
from random import shuffle
import os
import json

path_parsed = './data/sum_data/parsed/'
files = os.listdir(path_parsed)
file2doc = {}
files_abstract_as_summary = []
files_title_as_summary = []

for file in files:
    with open(os.path.join(path_parsed, file), 'r', encoding='UTF-8') as f:
        doc = json.load(f)
        if len(doc['article'].split()) > 5: #remove documents with empty articles
            file2doc[file] = doc
        if len(doc['article'].split()) > 5 and len(doc['title'].split()) > 1:
            files_title_as_summary.append(file)
        if len(doc['article'].split()) > 5 and len(doc['abstract'].split()) > 5:
            files_abstract_as_summary.append(file)

similar_docs = [] #documents with at least article, abstract or title in common
for el in ['article', 'abstract', 'title']:
    doc2file = {}
    for file in file2doc:
        if el == 'abstract' and len(file2doc[file]['abstract'].split()) < 5: #don't check very short abstracts
            continue
        if file2doc[file][el] not in doc2file:
            doc2file[file2doc[file][el]] = [file]
        else:
            doc2file[file2doc[file][el]].append(file)
    for value in doc2file.values():
        if len(value) > 1:
            similar_docs.append(tuple(sorted(value)))

similar_docs = set(similar_docs)

file_to_remove_duplicates = list(set([file for el in similar_docs for file in el[1:]]))

with open("list_of_duplicates.txt", 'w') as f:
    for el in similar_docs:
        f.write(','.join(el)+'\n')
    f.close()


with open('data/overlap/overlaps.json') as f:
    novel_words = json.load(f)

files_abstract_as_summary = list(set(novel_words.keys()).intersection(set(files_abstract_as_summary)))
files_title_as_summary = list(set(novel_words.keys()).intersection(set(files_title_as_summary)))

files_abstract_as_summary = [file for file in files_abstract_as_summary if file not in file_to_remove_duplicates]
files_title_as_summary = [file for file in files_title_as_summary if file not in file_to_remove_duplicates]

novel_1grams_per_abstract = sorted([float(novel_words[file]['h']['1']) for file in files_abstract_as_summary])

alpha = .9
percentile = novel_1grams_per_abstract[int(alpha * len(novel_1grams_per_abstract))]
print('Percentile: '+str(percentile))
files_abstract_as_summary = [file for file in files_abstract_as_summary if novel_words[file]['h']['1'] < percentile]


files_abstract_as_summary = [file for file in files_abstract_as_summary if file not in file_to_remove_duplicates]
files_title_as_summary = [file for file in files_title_as_summary if file not in file_to_remove_duplicates]


n_test = 10000
n_valid = 10000
n_train_abstract = len(files_abstract_as_summary) - n_valid - n_test
n_train_titles = len(files_title_as_summary) - n_valid - n_test

splits_abstract = ['test'] * n_test + ['valid'] * n_valid + ['train'] * n_train_abstract
splits_titles = ['test'] * n_test + ['valid'] * n_valid + ['train'] * n_train_titles
shuffle(splits_abstract)
shuffle(splits_titles)

def write_splits(files, splits, type_summary):
    split2file = {}
    assert len(files) == len(splits)
    for idx, split in enumerate(splits):
        if split not in split2file:
            split2file[split] = []
        split2file[split].append(files[idx])
    path = 'splits_{}_as_summary'.format(type_summary)
    if not os.path.isdir(path):
        os.mkdir(path)
    for split in split2file.keys():
        with open(os.path.join(path, '{}.txt'.format(split)), 'w') as f:
            f.write("\n".join(split2file[split]))
    f.close()

write_splits(files_abstract_as_summary, splits_abstract, 'abstract')
write_splits(files_title_as_summary, splits_titles, 'title')
