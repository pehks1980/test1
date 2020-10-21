import os

from django.core.files import File
from django.db import models

# Create your models here.
from urllib.request import urlretrieve, urlcleanup


class Images(models.Model):
    """
    Модель рисунка
    """
    document = models.FileField(upload_to='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    #Метод скачки файла по ссылке
    def download_to_local(self, url):
        try:
            name, _ = urlretrieve(url)
            f_name = os.path.basename(url)
            self.document.save(f_name, File(open(name, 'rb')))
        finally:
            #clear temp files after load
            urlcleanup()

