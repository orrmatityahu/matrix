
class Article(object):
    """
    Class to abstract Article from News site and normalize it.
    """

    def __init__(self, url, title, date, text):

        self.date = date
        self.title = title
        self.url = url
        self.text = text

    def to_dict(self):
        """
        :return: returns dict of object
        """
        return self.__dict__
