import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from selenium import webdriver

from api.classes.article import Article
from utils.system import get_file_path, get_file_name_by_os

SITE_URL = 'https://edition.cnn.com'


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
    title_tag = soup.find("h1", attrs={"class": "pg-headline"})

    # Check if Video Article( No Title ), if it is returns None
    if title_tag is None:
        return None
    title = title_tag.text

    # Date article published
    date_tag = soup.find("p", attrs={"class": "update-time"})
    date = date_tag.text.replace('Updated ', '')

    # Text of the article
    paragraphs = soup.find_all('div', attrs={"class": "zn-body__paragraph"})
    text = " ".join([paragraph.text for paragraph in paragraphs])

    return Article(url=url, title=title, date=date, text=text)


def get_html_page(url=SITE_URL):
    """
    get html page with selenium - Website includes Javascript
    :param url: url of news site - SITE_URL as default
    :return: html of site
    """

    # check if Site is reached
    try:
        requests.get(url)
    except ConnectionError:
        raise Exception('Could not reach CNN News')

    # get chromedriver-mac path
    chrom_driver_file_name = get_file_name_by_os()
    file_path = get_file_path(chrom_driver_file_name)

    # run browser and get html
    browser = webdriver.Chrome(file_path)
    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML")

    return innerHTML


def get_articles_tags():
    """
    get article tags from main site
    :return: articles tag array
    """

    main_page = get_html_page()

    soup = BeautifulSoup(main_page, 'html.parser')
    articles = soup.find_all('article')

    return articles


def create_articles():
    """
    create article objects array
    :return: articles object array
    """

    articles_tags = get_articles_tags()
    articles = []

    for article_tag in articles_tags:

        url = article_tag.attrs.get('data-vr-contentbox')

        final_url = '{}{}'.format(SITE_URL, url)
        if final_url == SITE_URL or not url:
            continue
        article = create_article_from_url(final_url)
        if article:
            articles.append(article)

    return articles
