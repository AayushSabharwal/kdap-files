from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from bs4 import BeautifulSoup as bsoup
import mwparserfromhell as mwph
import nltk
import requests


def diff_rev(rv1, rv2):
    url = 'https://en.wikipedia.org/w/api.php?action=compare&format=json&fromrev=' + rv1 + '&torev=' + rv2
    r = requests.get(url)
    data = r.json()
    soup = bsoup('<table>' + data['compare']['*'] + '</table>', 'lxml')
    additions = [bsoup(str(tag), 'lxml').text for tag in soup.find_all('ins', {'class': 'diffchange diffchange-inline'})]
    deletions = [bsoup(str(tag), 'lxml').text for tag in soup.find_all('del', {'class': 'diffchange diffchange-inline'})]
    return additions, deletions


def remove_punctuation(words):
    return [word for word in words if word not in ['.', '!', ',', ';', ':', '(', ')', '"', "'", '/', '-', '_', '=', '+',
                                                   "''", "'''", 'http', 'https', ',', '[', ']', '{', '}', '|', '\\', '"'
                                                   '``', '`', '<', '>', '--']]


def get_delta_data(changes):
    delta_data = {'words': 0, 'sentences': 0, 'wikilinks': 0}
    for change in changes:
        wikitext = mwph.parse(change)
        delta_data['wikilinks'] += len(wikitext.filter_wikilinks())

        cleaned_addition = change.replace('[[', '').replace(']]', '')
        sentences = nltk.sent_tokenize(cleaned_addition)
        print(sentences)
        delta_data['sentences'] += len(sentences)
        words = remove_punctuation(nltk.word_tokenize(cleaned_addition))
        print(words)
        delta_data['words'] += len(words)

    return delta_data


def revision_changes(article_name):
    revisions = get_revisions_of_article(article_name, rvprop='ids')[article_name]
    revisions.reverse()
    revisions_delta = {}
    for i in range(len(revisions) - 1):
        additions, deletions = diff_rev(str(revisions[i]['revid']), str(revisions[i+1]['revid']))
        add_data = get_delta_data(additions)
        del_data = get_delta_data(deletions)
        revisions_delta[revisions[i+1]['revid']] = {'additions': {}, 'deletions': {}}
        revisions_delta[revisions[i+1]['revid']]['additions'] = add_data
        revisions_delta[revisions[i+1]['revid']]['deletions'] = del_data

    return revisions_delta


'''
print(revision_changes('Talk:Evan Amos'))
'''
