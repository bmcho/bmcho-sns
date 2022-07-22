from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="수정일", auto_now=True)

    class Meta:
        abstract = True
