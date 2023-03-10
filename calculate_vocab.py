import nltk
import unicodedata
nltk.download('stopwords')
from nltk.corpus import stopwords
import spacy
import argparse

def is_punctuation(tok):
    if tok.isdigit():
        return True
    for c in tok:
        cp = ord(c)
        # We treat all non-letter/number ASCII as punctuation.
        # Characters such as "^", "$", and "`" are not in the Unicode
        # Punctuation class but we treat them as punctuation anyways, for
        # consistency.
        if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
            return True
        cat = unicodedata.category(c)
        if cat.startswith("P"):
            return True
        return False

parser = argparse.ArgumentParser()

parser.add_argument('--dataset_name', '-d_name', default=None, type=str, help="Name of GreekSum dataset. Either 'title' or 'abstract'")

args = parser.parse_args()

stopwords = stopwords.words('greek')
stopwords = set(stopwords)

nlp = spacy.load("el_core_news_sm")

stopwords.update(set(nlp.Defaults.stop_words))
vocab_doc=set()
vocab_sum = set()


train_doc = ""
val_doc = ""
test_doc = ""
train_sum = ""
val_sum = ""
test_sum = ""
if args.dataset_name.lower() == "title":
    train_doc = "./title/summarization_data_title/train-article.txt"
    val_doc = "./title/summarization_data_title/valid-article.txt"
    test_doc = "./title/summarization_data_title/test-article.txt"

    train_sum = "./title/summarization_data_title/train-title.txt"
    val_sum = "./title/summarization_data_title/valid-title.txt"
    test_sum = "./title/summarization_data_title/test-title.txt"
else:
    train_doc = "./abstract/summarization_data_abstract/train-article.txt"
    val_doc = "./abstract/summarization_data_abstract/valid-article.txt"
    test_doc = "./abstract/summarization_data_abstract/test-article.txt"

    train_sum = "./abstract/summarization_data_abstract/train-abstract.txt"
    val_sum = "./abstract/summarization_data_abstract/valid-abstract.txt"
    test_sum = "./abstract/summarization_data_abstract/test-abstract.txt"

doc_list = [train_doc,val_doc, test_doc]
sum_list = [train_sum,val_sum, test_sum]

for fl in doc_list:
    print("Preprocessing "+str(fl)+" file...")
    fr = open(fl,'r')
    for line in fr:
        line = line.strip()
        doc = nlp(line)
        for token in doc:
            lem = token.lemma_
            token=str(token).strip().lower()
            if (token not in stopwords and lem not in stopwords) and not is_punctuation(token):
                vocab_doc.add(lem)
    fr.close()

for fl in sum_list:
    print("Preprocessing "+str(fl)+" file...")
    fr = open(fl,'r')
    for line in fr:
        line = line.strip()
        doc = nlp(line)
        for token in doc:
            lem = token.lemma_
            token=str(token).strip().lower()
            if (token not in stopwords and lem not in stopwords) and not is_punctuation(token):
                vocab_sum.add(lem)
    fr.close()

print("Size of documents' vocabulary of GreekSUM "+args.dataset_name+": "+str(len(vocab_doc)))
print("Size of summaries' vocabulary of GreekSUM "+args.dataset_name+": "+str(len(vocab_sum)))
