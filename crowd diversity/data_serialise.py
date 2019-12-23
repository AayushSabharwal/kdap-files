from wikiExtract import wikiExtract
from kdap_wikiArticleRevisions import get_revisions_of_article
from wiki_get_article_quality import get_articles_quality
import json


def get_articles_in_wikiproj(proj):
    wikiProjectName = "Category:WikiProject_" + proj + "_articles"
    w = wikiExtract()



def get_all_articles_data(categories):
    # getting all the articles and quality data
    w = wikiExtract()
    all_articles = []
    articles = {}
    quality = {}
    for category in categories:
        wikiProjectName = "Category:WikiProject_" + category + "_articles"
        articles[category] = w.get_articles_by_category(category)[category]
        all_articles.extend(articles[category])
        category_articles_titles = [article['title'] for article in articles[category]]
        raw_quality = get_articles_quality(category_articles_titles, category)
        for article in raw_quality:
            quality[article] = raw_quality[article][category]['class']
    print(len(all_articles))
    print("A")
    # getting all revisions and editors of articles, removing articles with only one editor
    editors = {}
    all_editors = []
    revisions = {}
    for article in all_articles:
        revisions[article] = get_revisions_of_article(article, rvprop='ids|timestamp|flags|comment|user|sha1')[article]
        article_editors = []
        for revision in revisions[article]:
            if revision.get('user') is not None and revision['user'][-3:].lower() != 'bot':
                article_editors.append(revision['user'])
        article_editors = list(set(article_editors))

        if len(article_editors) < 2:
            print(article, article_editors)
            all_articles.remove(article)
            del revisions[article]
            for category in categories:
                if article in articles[category]:
                    articles[category].remove(article)
                    break
        else:
            editors[article] = article_editors
            all_editors.extend(article_editors)

    all_editors = list(set(all_editors))
    print("B")
    # getting article talk page edit history
    talk_page_edits = {}
    for article in all_articles:
        talk_page_edits[article] = get_revisions_of_article('Talk:' + article,
                                                            rvprop='ids|timestamp|flags|comment|user|sha1')
    print("C")
    # storing data as json
    with open("articles_data.json", "w") as fh:
        json.dump({"categories": categories,
                   "category_articles": articles,
                   "all_articles": all_articles,
                   "article_editors": editors,
                   "all_editors": all_editors,
                   "article_revisions": revisions,
                   "article_quality": quality,
                   "article_talk_page_edits": talk_page_edits}, fh)


get_all_articles_data(['Culture'])
