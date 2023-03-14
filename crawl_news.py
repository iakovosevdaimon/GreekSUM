# Script used to crawl the latest news from https://www.news247.gr/

from bs4 import BeautifulSoup
import requests
import csv
import time as timelibrary
from os import path

base_url = "https://www.news247.gr/<category>/?pages="
output_directory = "./"
categories = {"politiki": "politics", "koinonia": "society", "oikonomia": "economy", "politismos": "culture", "kosmos": "international"}
for category, category_fname in categories.items():
    news = open(path.join(output_directory, category_fname + ".csv"), "w")
    news_writer = csv.writer(news, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    news_writer.writerow(["title", "summary", "time", "url"])
    for i in range(1, 1000):
        html = requests.get(base_url.replace("<category>", category) + str(i)).content
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article")
        for article in articles:
            title = article.find("h3")
            if title:
                title = title.find("a")
            else:
                continue
            title_text = title["title"]
            title_href = title["href"]
            summary = article.find_all("div", {"class":"article__summary"})[0].find("p").text
            time = article.find("time")['datetime']
            news_writer.writerow([title_text, summary, time, title_href])
        timelibrary.sleep(5)
    news.close()
