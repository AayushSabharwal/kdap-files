from kdap_wikiArticlesEditedMonthwiseCount import get_monthwise_articles_edited_count
from kdap_wikiCategoryArticlesMonthwiseAuthors import get_monthly_authors_by_category
from kdap_wikiCategoryArticlesMonthwiseRevisions import get_monthly_revision_count_by_category
from matplotlib import pyplot as plt


def create_x_and_y(data, template_name):
    raw_timestamps = list(data[template_name].keys())
    raw_timestamps.sort()
    timestamps = []
    y_articles = []
    for timestamp in raw_timestamps:
        year = int(timestamp[:4])
        month = int(timestamp[5:])
        if 2009 <= year < 2016:
            timestamps.append(year + month / 12)
            y_articles.append(data[template_name][timestamp])

    return timestamps, y_articles


def get_graph(template_name):
    plt.clf()
    articles_edited_count = get_monthwise_articles_edited_count(template_name)
    monthly_authors_count = get_monthly_authors_by_category(template_name)
    revisions_count = get_monthly_revision_count_by_category(template_name)
    for timestamp in monthly_authors_count[template_name]:
        monthly_authors_count[template_name][timestamp] = len(monthly_authors_count[template_name][timestamp])

    print(articles_edited_count[template_name])
    timestamps, y_articles = create_x_and_y(articles_edited_count, template_name)
    print(timestamps)
    print(y_articles)
    print([(timestamps[i], y_articles[i]) for i in range(len(timestamps))])
    sorted_keys = sorted(articles_edited_count[template_name].keys())
    print([(sorted_keys[i], articles_edited_count[template_name][sorted_keys[i]]) for i in range(len(sorted_keys))])
    plt.plot(timestamps, y_articles, label='Articles')

    timestamps, y_articles = create_x_and_y(monthly_authors_count, template_name)
    plt.plot(timestamps, y_articles, label='Authors')

    timestamps, y_articles = create_x_and_y(revisions_count, template_name)
    plt.plot(timestamps, y_articles, label='Revisions')

    plt.yscale('log')
    plt.legend(loc='best')
    plt.show()


get_graph('Black Lives Matter')