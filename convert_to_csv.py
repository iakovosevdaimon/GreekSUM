import pandas as pd


def convert_to_csv(dic, task_d):
    for k in dic.keys():
        texts = []
        labels = []
        with open(dic.get(k)[0], 'r') as fr_text, open(dic.get(k)[1], 'r') as fr_labels:
            for line1, line2 in zip(fr_text, fr_labels):
                if line1.strip() and line2.strip():
                    line1 = line1.strip()
                    line1 = line1.replace('\n','')
                    line2 = line2.strip()
                    line2 = line2.replace('\n','')
                    texts.append(line1)
                    labels.append(line2)
        df = pd.DataFrame(list(zip(texts, labels)), columns =['Article', task_d])
        path = './'+str(task_d.lower())+'/summarization_data_'+str(task_d.lower())+'/'+str(k)+'.csv'
        df.to_csv(path, index=False)


train_file = "./abstract/summarization_data_abstract/train-article.txt"
train_labels_file = "./abstract/summarization_data_abstract/train-abstract.txt"

valid_file = "./abstract/summarization_data_abstract/valid-article.txt"
valid_labels_file = "./abstract/summarization_data_abstract/valid-abstract.txt"

test_file = "./abstract/summarization_data_abstract/test-article.txt"
test_labels_file = "./abstract/summarization_data_abstract/test-abstract.txt"

dic = {'train':[train_file, train_labels_file], "valid":[valid_file, valid_labels_file], "test":[test_file, test_labels_file]}

convert_to_csv(dic, 'Abstract')


train_file = "./title/summarization_data_title/train-article.txt"
train_labels_file = "./title/summarization_data_title/train-title.txt"

valid_file = "./title/summarization_data_title/valid-article.txt"
valid_labels_file = "./title/summarization_data_title/valid-title.txt"

test_file = "./title/summarization_data_title/test-article.txt"
test_labels_file = "./title/summarization_data_title/test-title.txt"

dic = {'train':[train_file, train_labels_file], "valid":[valid_file, valid_labels_file], "test":[test_file, test_labels_file]}
convert_to_csv(dic, 'Title')
