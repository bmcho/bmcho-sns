from django.db import models

from apps.core.models import TimeStampModel

# Create your models here.
class Review(TimeStampModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    review = models.CharField(max_length=2000, null=False)
