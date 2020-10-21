
from django import forms
from .models import Images

class ImageUploadForm(forms.ModelForm):
    """
    Форма загрузки рисунка
    """
    url_link = forms.CharField(label='URL линк на картинку', max_length=256, required=False)

    class Meta:
        model = Images
        fields = ('document',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document'].label = "Имя файла"

    # Валидация формы загрузки, на наличие URL линка или файла
    def clean(self):
        cleaned_data = super().clean()
        url_link = cleaned_data.get("url_link")
        document = cleaned_data.get("document")

        if url_link == '':
            if document is None:
                raise forms.ValidationError("Укажите какое-нибудь одно поле - либо URL линк, либо имя файла")

            if document.name[-3:] != 'jpg' and document.name[-3:] != 'png':
                raise forms.ValidationError("Имя файла *.jpg или  *.png")

        elif document is not None:
            raise forms.ValidationError("Укажите только одно поле - либо URL линк, либо имя файла")

        return cleaned_data


class ImageViewForm(forms.Form):
    """
    Форма просмотра рисунка
    """
    size_x = forms.CharField(label='x image size', max_length=10)
    size_y = forms.CharField(label='y image size', max_length=10)