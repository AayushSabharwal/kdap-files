import json


def get_all_bots():
    with open("articles_data.json", "r") as fh:
        all_data = json.load(fh)

    bots = all_data['all_bots']
    return bots


def get_editors_of_article(article):
    with open("articles_data.json", "r") as fh:
        all_data = json.load(fh)

    revisions = all_data['article_revisions'][article]
    all_editors = all_data['all_editors']
    editors = []
    for revision in revisions:
        if 'user' in revision.keys() and revision['user'] in all_editors:
            editors.append(revision['user'])

    return editors
