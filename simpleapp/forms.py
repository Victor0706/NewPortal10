from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewForm(forms.ModelForm):
    text = forms.CharField(min_length=5)

    class Meta:
        model = Post
        fields = ['title', 'text', 'rating', 'author', 'postCategory']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class ArticleForm(forms.ModelForm):
    text = forms.CharField(min_length=5)

    class Meta:
        model = Post
        fields = ['title', 'text', 'rating', 'author', 'postCategory']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data