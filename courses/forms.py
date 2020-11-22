from django import forms
from django.contrib.auth.models import User
from .models import Category, Course, Lesson



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['Title', 'Description', 'Image']
        help_texts = {
            'Title': 'Mysal üçin Geometriýa, Matematika we ş.m.',
            'Description':'Kategoriýanyň gysgaça düşündirilişini giriziň',
            'Image':'Kategoriýanyň suratyny goýup bilersiňiz'
        }
        labels = {
            'Title':'Ady',
            'Description':'Düşündiriş',
            'Image':'Surat',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['Creator','slug', 'Title', 'Category', 'Description', 'Image', 'Level', ]
        help_texts = {
            'Title': 'Kursuňyzyň adyny giriziň',
            'Description':'Kursuň gysgaça beýanyny goýuň',
            'Category':'Kurs döredjek kategoriýany saýlaň',
            'Level':'Kursuňyza bir dereje girizin',
            'Image':'Kursuň suratyny goýup bilersiňiz ýa-da boş goýup bilersiňiz',
        }
        labels = {
            'Title':'Ady',
            'Description':'Düşündiriş',
            'Category':'Kategoriýa',
            'Level':'Dereje',
            'Image':'Surat',

        }
        widgets = {'Creator': forms.HiddenInput(), 'slug': forms.HiddenInput()}


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['slug','Title', 'Course', 'Video_id', 'Position', ]
        help_texts = {
            'Title':'Sapagyň adyny giriziň',
            'Kurs':'Bu sapagyň kursuny saýlaň',
            'Video_id':'Video sapagyny saýlaň',
            'Position':'Sapak tertibini giriziň'
        }
        labels = {
            'Title':'Ady',
            'Course':'Kurs',
            'Position':'Tertibi',
        }
        widgets = {
            'slug': forms.HiddenInput()
        }
