from djongo.storage import GridFSStorage
from django.db import models
from django.conf import settings

grid_fs_storage = GridFSStorage(collection='myfiles', base_url='/media/myfiles/')

class Pdf(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to='pdfs', storage=grid_fs_storage)


class VideoMetadata(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to='pdfs', storage=grid_fs_storage)
    title = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
