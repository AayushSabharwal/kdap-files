from wikiExtract import wikiExtract
from kdap_wikiArticleRevisions import get_revisions_of_article
from wiki_get_article_quality import get_articles_quality
import json
import requests


def get_all_articles_data(categories):
    # getting all the articles and quality data
    with open("sample_articles.txt", "r") as fh:
        all_articles = [article.strip() for article in fh.readlines()][:100]

    articles_quality = {}
    category_articles = {}
    for article in all_articles:
        if article[:14].lower() == 'category talk:':
            all_articles.remove(article)
        if article[:11].lower() == 'draft talk:':
            all_articles.remove(article)

    for article in all_articles:
        quality = get_articles_quality(article)
        if article in quality.keys():
            for category in quality:
                if category in categories:
                    if category in category_articles.keys():
                        category_articles[category].append(article)
                    else:
                        category_articles[category] = [article]
                    quality = {category: quality[category]['class']}
                    break
            if len(quality.keys()) != 1:
                print("Quality error:", article, quality)
                all_articles.remove(article)
            else:
                articles_quality[article] = quality
        else:
            all_articles.remove(article)
            print(article, quality)

    # getting all bots
    all_bots = []
    url = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=allusers&augroup=bot"
    while True:
        r = requests.get(url)
        data = r.json()
        all_bots.extend([bot['name'] for bot in data['query']['allusers']])

        if data.get('continue') is not None:
            url = url + '&aufrom=' + data['continue']['aufrom']
        else:
            break

    # getting all revisions and editors of articles, removing articles with only one editor
    editors = {}
    all_editors = []
    revisions = {}
    for article in all_articles:
        revisions[article] = get_revisions_of_article(article, rvprop='ids|timestamp|flags|comment|user|sha1')[article]
        article_editors = []
        for revision in revisions[article]:
            if revision.get('user') is not None and revision['user'] not in all_bots:
                article_editors.append(revision['user'])
        article_editors = list(set(article_editors))

        if len(article_editors) < 2:
            print(article, article_editors)
            all_articles.remove(article)
            del revisions[article]
            for category in categories:
                if article in category_articles[category]:
                    category_articles[category].remove(article)
                    break
        else:
            editors[article] = article_editors
            all_editors.extend(article_editors)

    all_editors = list(set(all_editors))

    # getting article talk page edit history
    talk_page_edits = {}
    for article in all_articles:
        talk_page_edits[article] = get_revisions_of_article('Talk:' + article,
                                                            rvprop='ids|timestamp|flags|comment|user|sha1')

    # storing data as json
    with open("articles_data.json", "w") as fh:
        json.dump({"categories": categories,
                   "category_articles": category_articles,
                   "all_articles": all_articles,
                   "article_editors": editors,
                   "all_editors": all_editors,
                   "all_bots": all_bots,
                   "article_revisions": revisions,
                   "article_quality": articles_quality,
                   "article_talk_page_edits": talk_page_edits}, fh)


get_all_articles_data(['Geography', 'History', 'Philosophy', 'Religion', 'Mathematics', 'Sociology', 'Technology',
                       'Science', 'Culture'])
