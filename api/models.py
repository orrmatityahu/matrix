from django.db import models


class Article(models.Model):
    url = models.CharField(max_length=128, unique=True)
    date = models.CharField(max_length=256)
    text = models.TextField(max_length=4096)
    title = models.CharField(max_length=256)


class Scan(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=128, default='started')
    status_message = models.TextField(max_length=4096, default='')
