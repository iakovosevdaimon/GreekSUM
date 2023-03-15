# GreekSUM Dataset

We introduce the first Greek summarization dataset, created by scrapping the ["News24/7" website](https://www.news247.gr/). News24/7 is one of the leading news websites in Greece, part of the [24 MEDIA digital publishing group](https://www.24media.gr/). We collected data from web pages that span from October 2007 to June 2022, covering five major categories: politics, society, economy, culture, and world. Each article had a one-sentence title and a succinct abstract, features which were extracted, yielding two summarization tasks: GreekSUM Title and GreekSUM Abstract. </br>

Moreover, we produce a classification dataset by taking into account the five separate subjects to which an article is assigned, as labels for this dataset. </br>


As a post-processing step, we filtered the scrapped pages, removing all empty articles and articles whose titles were shorter than 2 words or whose abstracts were less than 5 words. Secondly, we filtered the duplicated articles (i.e., articles with the same body, or with the same title, or with the same abstract), as an article can belong to more than one category, and thus be crawled multiple times. Finally, we noticed that several abstracts looked more like introductions rather than actual summaries of the article. Therefore, we eliminated 10% of the articles with the highest proportion of novel unigrams in the abstracts. This corresponded to a threshold of 46.7% novel unigrams. </br>

For both proposed summarization tasks, we reserved 10k pairs for testing, 10k for validation, and all the remaining pairs for training. </br>


We do not publish directly the dataset, but you can reproduce it by using our code. </br>


### Steps to create the dataset
Starting from an empty directory structure, run the following scripts, in that order.
1. "crawl_news.py"
1. "crawl_articles.py"
1. "generate_GreekSUM.sh"

### Extra scripts

Use "calculate_vocab.py" script to compute the size of the vocabulary for GreekSUM Title and GreekSUM Abstract. </br>

The purpose of the script called "novel_ngrams_predictions.py" is to determine the percentage of novel n-grams that are introduced by the machine-generated summaries in comparison to the reference summaries. </br>

Finally, the script "statistics.py" is utilized to obtain various statistics about the GreekSUM Title and the GreekSUM Abstract. These include the length of the articles and reference summaries, as well as the percentage of n-gram sequences found in the reference summaries but not in the article body.
