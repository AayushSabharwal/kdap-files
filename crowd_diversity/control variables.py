from crowd_diversity.utility_functions import get_editors_of_article, get_revisions_of_article
from crowd_diversity.wiki_get_editor_contribution import get_editor_contribution_to_wikipedia
import datetime
import math


def article_size(article):
    editors = set(get_editors_of_article(article))
    return math.log10(len(editors))


def article_age(article):
    revisions = get_revisions_of_article(article)
    timestamp = revisions[len(revisions) - 1]['timestamp']
    creation_date = datetime.datetime(int(timestamp[:4]), int(timestamp[5:7]), int(timestamp[8:10]))
    now_date = datetime.datetime(2016, 4, 1)
    return math.log10((now_date - creation_date).total_seconds())


def average_experience(article):
    editors = list(set(get_editors_of_article(article)))
    average = 0
    for editor in editors:
        average += get_editor_contribution_to_wikipedia(editor)

    average /= len(editors)
    return math.log10(average)


'''
print(article_age('Gammoid'))
print(article_size('Gammoid'))
print(average_experience('Gammoid'))
'''
