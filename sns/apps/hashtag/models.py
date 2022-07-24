from statistics import mode

from django.db import models

from apps.core.models import TimeStampModel


# Create your models here.
class Hashtag(TimeStampModel):
    hashtag_name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f'{self.hashtag_name}'
