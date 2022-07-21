from django.db import models
from apps.core.models import TimeStampModel


# Create your models here.
class Post(TimeStampModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    contents = models.TextField(null=False)

class PostLike(TimeStampModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)


