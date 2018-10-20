from api.models import Article
from utils import cnn_frontend as cnn
from utils import fox_frontend as fox


def scan(*, scan_obj):
    """
    Scan News sites and update scan obj
    :param scan_obj: scan obj to update
    :return: scan_obj
    """
    try:
        cnn_articles = cnn.create_articles()
        fox_articles = fox.create_articles()

        articles = fox_articles + cnn_articles

        for article in articles:
            article_dict = article.to_dict()
            Article.objects.update_or_create(defaults=article_dict, url=article_dict.get('url'))

        scan_obj.status = 'completed'
        scan_obj.save()

    except Exception as e:
        scan_obj.status = 'failed'
        scan_obj.status_message = str(e)
        scan_obj.save()

    return scan_obj
