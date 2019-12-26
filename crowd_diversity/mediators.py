from crowd_diversity.utility_functions import get_revisions_of_article, get_article_talk_page_revisions
import math


def task_conflict(article):
    revisions = get_revisions_of_article(article)
    hash_frequency = {}
    for revision in revisions:
        if revision['sha1'] not in hash_frequency:
            hash_frequency[revision['sha1']] = 0
        hash_frequency[revision['sha1']] += 1

    reverts = 0
    for sha1 in hash_frequency:
        reverts += hash_frequency[sha1] - 1

    return reverts/len(revisions)


def task_communication(article):
    talk_revisions = get_article_talk_page_revisions(article)
    return math.log10(len(talk_revisions))


'''
print(task_communication('Gammoid'))
print(task_conflict('Gammoid'))
'''
