from djongo.storage import GridFSStorage
from django.db import models
from django.conf import settings

grid_fs_storage = GridFSStorage(collection='myfiles', base_url='/media/myfiles/')

class Pdf(models.Model):
    file = models.FileField(upload_to='pdfs', storage=grid_fs_storage)
