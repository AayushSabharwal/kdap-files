from kdap_wikiArticlesEditedMonthwiseCount import get_monthwise_articles_edited_count
from kdap_wikiCategoryArticlesMonthwiseAuthors import get_monthly_authors_by_category
from kdap_wikiCategoryArticlesMonthwiseRevisions import get_monthly_revision_count_by_category
from matplotlib import pyplot as plt


def create_x_and_y(data, template_name):
    timestamps = []
    y_articles = []
    for timestamp in data[template_name]:
        year = int(timestamp[:4])
        month = int(timestamp[5:])
        timestamps.append(year + month / 12)
        y_articles.append(data[template_name][timestamp])

    return  timestamps, y_articles


def get_graph(template_name):
    plt.clf()
    articles_edited_count = get_monthwise_articles_edited_count(template_name)

    monthly_authors_count = get_monthly_authors_by_category(template_name)
    revisions_count = get_monthly_revision_count_by_category(template_name)

    for timestamp in monthly_authors_count[template_name]:
        monthly_authors_count[template_name][timestamp] = len(monthly_authors_count[template_name][timestamp])
    print(len(articles_edited_count[template_name]), len(monthly_authors_count[template_name]), len(revisions_count[template_name]))

    timestamps, y_articles = create_x_and_y(articles_edited_count, template_name)
    plt.plot(timestamps, y_articles)

    timestamps, y_articles = create_x_and_y(monthly_authors_count, template_name)
    plt.plot(timestamps, y_articles)

    timestamps, y_articles = create_x_and_y(revisions_count, template_name)
    plt.plot(timestamps, y_articles)
    plt.show()


get_graph('Black Lives Matter')