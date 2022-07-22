from statistics import mode
from django.db import models

from apps.core.models import TimeStampModel

# Create your models here.
class Hashtag(TimeStampModel):
    hashtag_name = models.CharField(max_length=50, null=False)
    post = models.ManyToManyField('post.Post', related_name="hashtags")

