from django.db import models

from apps.core.models import TimeStampModel


# Create your models here.
class Post(TimeStampModel):
    user = models.ForeignKey("user.User", related_name='posting', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    contents = models.TextField(null=False)
    hits = models.IntegerField(default=0)
    hashtag = models.ManyToManyField('hashtag.Hashtag', related_name="posting")


class PostLike(TimeStampModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
