import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

from api.classes.article import Article

SITE_URL = 'https://www.foxnews.com/'


def create_article_from_url(url):
    """
    Create an Article object from url of article
    :param url: url of article
    :return: Article(object) with data
    """
    try:
        response = requests.get(url)
    except ConnectionError:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')

    # title of article
    title_tag = soup.find("h1", attrs={"class": "headline"})

    # Check if Video Article, if it is returns None
    if title_tag is None:
        return None
    title = title_tag.text

    # Date article published
    date_tag = soup.find("div", attrs={"class": "article-date"})
    date = date_tag.text.replace('Published', '')

    # Text of the article
    article_body = soup.find('div', attrs={'class': 'article-body'})
    paragraphs = article_body.findChildren('p')
    text = " ".join([paragraph.text for paragraph in paragraphs])

    return Article(url=url, title=title, date=date, text=text)


def get_articles_tags(url=SITE_URL):
    """
    get article tags array
    :param url: url of news site
    :return: article tags array
    """

    # check if news site is reachable
    try:
        response = requests.get(url)
    except ConnectionError:
        raise Exception('Could not reach FoxNews')

    # find all articles by article tag from main div
    soup = BeautifulSoup(response.content, 'html.parser')
    main = soup.find('div', attrs={'class': 'page-content'})
    articles = main.find_all('article')

    return articles


def get_articles_urls():
    """
    get articles urls
    :return: articles urls array
    """
    articles_tags = get_articles_tags()

    article_urls = []

    for article_tag in articles_tags:
        link = article_tag.find('a')
        article_urls.append(link.attrs.get('href'))

    return article_urls


def create_articles():
    """
    create articles object array
    :return: articles object array
    """

    articles_urls = get_articles_urls()
    articles = []

    for url in articles_urls:

        # Videos are in other domain
        if not url or SITE_URL not in url or url == SITE_URL:
            continue
        article = create_article_from_url(url)
        if article:
            articles.append(article)

    return articles