from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from config.models import BasedModel


class Image(BasedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption if self.caption else f'Image for {self.content_object}'
