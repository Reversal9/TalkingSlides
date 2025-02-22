from djongo.storage import GridFSStorage
from django.db import models
from django.conf import settings

grid_fs_storage = GridFSStorage(collection='myfiles', base_url='/media/myfiles/')

class Pdf(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to='pdfs', storage=grid_fs_storage)
