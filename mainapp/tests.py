# Create your tests here.
import os

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from mainapp.models import Images


class TestMainappSmoke(TestCase):
    def setUp(self):
        self.client = Client()

    def test_mainapp_urls(self):
        """
        Проверка страниц на открывание
        """
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/upload_page/')
        self.assertEqual(response.status_code, 200)

    def test_upload_url_and_view(self):
        """
        Проверка загрузки картинки по ссылке и открывание страницы ее редактирования
        """
        url_link = 'https://icdn.lenta.ru/images/2020/08/24/07/20200824073813167/top7_5c361045e33332b45dce3d8474e8de47.jpg'

        image = Images()
        image.download_to_local(url_link)
        image.save()

        response = self.client.get('/view_page/1/')
        self.assertEqual(response.status_code, 200)

    def test_no_yes_file_chosen(self):
        """
        Проверка страницы формы загрузки

        """
        response = self.client.post(
            "/upload_page/", data=dict(document="", url_link="")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Укажите какое-нибудь одно поле - либо URL линк, либо имя файла", html=True)

        #make fake file to test upload file name
        try:
            with open('test.txt', 'wb') as F:
                F.write(b"123")
        finally:
            F.close()

        file_path = F.name

        f = open(file_path, "r")

        response = self.client.post(
            "/upload_page/", data=dict(document=f, url_link="car")
        )
        f.close()

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Укажите только одно поле - либо URL линк, либо имя файла", html=True)

        f = open(file_path, "r")
        response = self.client.post(
            "/upload_page/", data=dict(document=f, url_link="")
        )
        f.close()

        self.assertEqual(response.status_code, 200)

        #print(response.content.decode('utf8'))

        self.assertContains(response, "Имя файла *.jpg или  *.png", html=True)

        os.remove(f.name)

    def tearDown(self):
        pass