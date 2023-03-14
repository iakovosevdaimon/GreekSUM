# Script used to crawl news articles from https://www.news247.gr/ . 
# crawl_news.py has to be executed before hand 

from bs4 import BeautifulSoup
import requests
import csv
import time as timelibrary
from os import path

input_directory = "./"
output_directory = "crawled_articles"

if not path.isdir(output_directory):
    os.mkdir(output_directory)

for category in ["politics", "society", "economy", "culture", "international"]:
    news = open(path.join(input_directory, category + ".csv"), "r")
    news_reader = csv.reader(news, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    row_number = -1
    for row in news_reader:
        row_number += 1
        if row_number < 1:
            continue
        fname = "crawled_articles/" + category + "_" + str(row_number)
        if path.exists(fname):
            continue
        html = requests.get(row[-1]).content
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find_all("div", {"class":"article-body__body"})
        if not article:
            temp = open(fname, 'w')
            temp.close()
            continue
        article = article[0]
        text = []
        for paragraph in article.find_all("p"):
            text.append(paragraph.text) 
        with open(fname, 'w') as f:
            f.write("\n".join(text))
        timelibrary.sleep(5)
    news.close()
