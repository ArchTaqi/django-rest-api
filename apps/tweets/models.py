from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.likes import Like


class Tweet(models.Model):
    body = models.CharField(max_length=140)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.body

    @property
    def total_likes(self):
        return self.likes.count()
