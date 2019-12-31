from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from mwviews.api import PageviewsClient
import datetime


def find_correlation(article_name):
    revisions = get_revisions_of_article(article_name, rvprop='ids|timestamp')[article_name]
    revisions.reverse()
    start_date = datetime.datetime(int(revisions[0]['timestamp'][:4]), int(revisions[0]['timestamp'][5:7]),
                                   int(revisions[0]['timestamp'][8:10]))
    end_date = datetime.datetime(int(revisions[-1]['timestamp'][:4]), int(revisions[-1]['timestamp'][5:7]),
                                 int(revisions[-1]['timestamp'][8:10]))
    PageviewsClient.article_views('en.wikipedia')