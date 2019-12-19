from wiki_pageViews import get_pageviews
from matplotlib import pyplot as plt


def get_pageview_graph(articles):
    pageviews = {}
    for article in articles:
        pageviews[article] = []

