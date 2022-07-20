from django.db import models
from sns.apps.core.models import TimeStampModel


# TODO: 아직 작성 할것 많이 남음
# Create your models here.
class Post(TimeStampModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    contents = models.TextField(null=False)

