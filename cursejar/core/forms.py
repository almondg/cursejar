from allauth import models
from django.shortcuts import render
from djangotoolbox.fields import ListField
from core.models import Author, Book

__author__ = 'shaked'

from django import forms
from django.forms.models import inlineformset_factory
from .models import Challenge, Word


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge


class WordForm(forms.ModelForm):
    class Meta:
        model = Word

ChallengeFormSet = inlineformset_factory(Challenge, Word)


class StringListField(forms.CharField):
    def prepare_value(self, value):
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]


class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)


class MyForm(forms.Form):
    original_field = forms.CharField()
    extra_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(extra_fields):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = \
                forms.CharField()

    def myview(request):
        if request.method == 'POST':
            form = MyForm(request.POST, extra=request.POST.get('extra_field_count'))
            if form.is_valid():
                print "valid!"
            else:
                form = MyForm()
        return render(request, "template", { 'form': form })


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book

BookFormSet = inlineformset_factory(Author, Book)