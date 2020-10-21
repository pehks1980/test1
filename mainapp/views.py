from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mainapp.forms import ImageUploadForm, ImageViewForm
from mainapp.models import Images
from django.views.decorators.csrf import csrf_exempt
import base64
from io import BytesIO
from PIL import Image


# Create your views here.

def main(request):
    """
    Заглавная страница - список файлов
    """
    title = 'Главная - список файлов'
    # get links from db
    links = Images.objects.all()

    content = {'title': title, 'links': links}

    return render(request, 'mainapp/index.html', content)


@csrf_exempt
def upload_page(request):
    """
    Контроллер загрузки рисунка
    """
    title = 'Загрузка рисунка'

    if request.method == 'POST':
        # file request.Files
        upload_form = ImageUploadForm(request.POST, request.FILES)

        if upload_form.is_valid():
            url_link = request.POST.get('url_link')
            if url_link != '':
                # В случае линка
                image = Images()
                image.download_to_local(url_link)
                image.save()
            else:
                # в cлучае файла
                upload_form.save()
            return HttpResponseRedirect(reverse('main'))


    else:  # GET
        upload_form = ImageUploadForm()

    content = {'title': title, 'upload_form': upload_form}

    return render(request, 'mainapp/upload_form.html', content)


@csrf_exempt
def view_page(request, pk):
    """
    Контроллер страницы просмотра и изменения размеров рисунка
    """
    title = 'Просмотр. изменение размеров рисунка'

    if request.method == 'POST':
        # file request.Files
        view_form = ImageViewForm(request.POST)

        if view_form.is_valid():
            # Если размер изменен, рассчитываем новый размер, делаем его ресайз (от текущего current), декодируем в base64,
            # добавляем заголовок картинки (PNG)
            new_size_x = int(request.POST['size_x'])
            new_size_y = int(request.POST['size_y'])
            current_size_x = int(request.POST['current_size_x'])
            current_size_y = int(request.POST['current_size_y'])

            image = Images.objects.get(id=int(pk))

            _image = Image.open(image.document)

            if new_size_x != current_size_x:
                # new_size_x changed
                new_size_y = int((current_size_y * new_size_x) / current_size_x)
            else:
                if new_size_y != current_size_y:
                    # new_size_y changed
                    new_size_x = int((current_size_x * new_size_y) / current_size_y)

            new_size = (new_size_x, new_size_y)

            _image = _image.resize(new_size)

            data = {'size_x': f'{_image.size[0]}', 'size_y': f'{_image.size[1]}'}
            view_form = ImageViewForm(initial=data)

            buffered = BytesIO()
            _image.save(buffered, format="PNG")
            img_byte = base64.b64encode(buffered.getvalue())

            image_decoded = "data:image/png;base64," + img_byte.decode()

            content = {'title': title, 'view_form': view_form, 'pk': int(pk), 'image': image_decoded, \
                       'image_x': new_size_x, 'image_y': new_size_y}

            return render(request, 'mainapp/view_page.html', content)

    else:  # GET
        # загружаем картинку и выводим в форму ее размеры
        image = Images.objects.get(id=int(pk))

        _image = Image.open(image.document)

        data = {'size_x': f'{_image.size[0]}', 'size_y': f'{_image.size[1]}'}
        view_form = ImageViewForm(initial=data)
        # распаковываем картинку в массив, декодируем в base64 добавляем заголовок картинки (PNG)
        buffered = BytesIO()
        _image.save(buffered, format="PNG")
        img_byte = base64.b64encode(buffered.getvalue())

        image_decoded = "data:image/png;base64," + img_byte.decode()

    content = {'title': title, 'view_form': view_form, 'pk': int(pk), 'image': image_decoded, \
                   'image_x': _image.size[0], 'image_y': _image.size[1]}

    return render(request, 'mainapp/view_page.html', content)
