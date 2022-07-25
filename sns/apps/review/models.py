from django.db import models

from apps.core.models import TimeStampModel


# Create your models here.
class Review(TimeStampModel):
    post = models.ForeignKey('post.Post', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', related_name='reviews', on_delete=models.CASCADE)
    review = models.CharField(null=False, max_length=200)
