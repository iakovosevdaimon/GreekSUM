import os
import json
import re

def generate_dataset(in_path, to_path, dataset_type):

    path_dir = "./data/sum_data/parsed"
    train_file=os.path.join(in_path,'train.txt')
    valid_file=os.path.join(in_path,'valid.txt')
    test_file=os.path.join(in_path,'test.txt')

    train_task_path = os.path.join(to_path,'train-{}.txt'.format(dataset_type))
    train_article_path = os.path.join(to_path,'train-article.txt')

    valid_task_path = os.path.join(to_path,'valid-{}.txt'.format(dataset_type))
    valid_article_path = os.path.join(to_path,'valid-article.txt')

    test_task_path = os.path.join(to_path,'test-{}.txt'.format(dataset_type))
    test_article_path = os.path.join(to_path,'test-article.txt')

    dc = {"train":[train_file, train_task_path, train_article_path], "valid":[valid_file, valid_task_path, valid_article_path], "test":[test_file, test_task_path, test_article_path]}
    for k in dc.keys():
        lst = dc.get(k)
        fr = open(lst[0],"r")
        fw_task = open(lst[1],"w")
        fw_article = open(lst[2],"w")
        for line in fr:
            with open(os.path.join(path_dir, line.strip()), 'r', encoding='UTF-8') as f:
                doc = json.load(f)
                art = doc["article"].strip()
                art = art.replace("\n"," ")
                if not re.match(".*[.!;:,·]$", art):
                    art = art+'.'
                task_d = doc[dataset_type].strip()
                task_d = task_d.replace("\n"," ")
                if dataset_type =="abstract":
                    if not re.match(".*[.!;:,·]$", task_d):
                        task_d = task_d+'.'
                fw_task.write(task_d+"\n")
                fw_article.write(art+"\n")
        fr.close()
        fw_task.close()
        fw_article.close()




def generate_classification(in_path, to_path):

    path_dir = "./data/sum_data/parsed"
    train_file=os.path.join(in_path,'train.txt')
    valid_file=os.path.join(in_path,'valid.txt')
    test_file=os.path.join(in_path,'test.txt')

    train_task_path = os.path.join(to_path,'train.sent')
    train_label_path = os.path.join(to_path,'train.label')

    valid_task_path = os.path.join(to_path,'valid.sent')
    valid_label_path = os.path.join(to_path,'valid.label')

    test_task_path = os.path.join(to_path,'test.sent')
    test_label_path = os.path.join(to_path,'test.label')

    dc = {"train":[train_file, train_task_path, train_label_path], "valid":[valid_file, valid_task_path, valid_label_path], "test":[test_file, test_task_path, test_label_path]}
    categories = ["economy","politics","society","international","culture"]
    category2id = {k:i for i, k in enumerate(categories)}
    id2category = {i:k for i, k in enumerate(categories)}
    with open(os.path.join(to_path,"classification_labels.json"), "w") as outfile:
        json.dump(id2category, outfile)

    for k in dc.keys():
        lst = dc.get(k)
        fr = open(lst[0],"r")
        fw_task = open(lst[1],"w")
        fw_label = open(lst[2],"w")
        for line in fr:
            with open(os.path.join(path_dir, line.strip()), 'r', encoding='UTF-8') as f:
                doc = json.load(f)
                art = doc["article"].strip()
                art = art.replace("\n"," ")
                if not re.match(".*[.!;:,·]$", art):
                    art = art+'.'
                fw_task.write(art+"\n")
                fw_label.write(str(category2id[doc["label"]])+"\n")
        fr.close()
        fw_task.close()
        fw_label.close()



path_split_title="./splits_title_as_summary"
path_split_abstract="./splits_abstract_as_summary"

path_title="./title/summarization_data_title"
path_abstract="./abstract/summarization_data_abstract"
path_classification="./classification"

if not os.path.isdir(path_classification):
        os.mkdir(path_classification)
        os.mkdir(os.path.join(path_classification,'data'))

path_classification=os.path.join(path_classification,'data')

generate_dataset(path_split_title, path_title, "title")
generate_dataset(path_split_abstract, path_abstract, "abstract")
generate_classification(path_split_title, path_classification)
