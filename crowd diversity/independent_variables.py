import math
import statistics
from utility_functions import get_editors_of_article, get_all_bots
from wiki_get_editor_contribution import get_editor_contribution_to_wikipedia


def contribution_diversity(article):
    editors = get_editors_of_article(article)
    bots = get_all_bots()
    for editor in editors:
        if editor in bots:
            editors.remove(editor)

    distinct_editors = list(set(editors))
    freq = []
    for editor in distinct_editors:
        freq.append(editors.count(editor))

    diversity = math.log10((statistics.pvariance(freq)) ** 0.5 / statistics.mean(freq) * 100)
    return diversity


def experience_diversity(article):
    editors = list(set(get_editors_of_article(article)))
    bots = get_all_bots()
    for editor in editors:
        if editor in bots:
            editors.remove(editor)

    print(len(editors))
    freq = []
    for editor in editors:
        print(editor)
        freq.append(get_editor_contribution_to_wikipedia(editor))

    diversity = math.log10((statistics.pvariance(freq)) ** 0.5 / statistics.mean(freq) * 100)
    return diversity


print(experience_diversity('Conical surface'))