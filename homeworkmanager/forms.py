from django import forms
from django.contrib.admin import widgets as adminwidgets

from homeworkmanager.models import Homework, HomeworkComment, Subject

class HomeworkForm(forms.ModelForm):
    """Form for creating/editing one homework."""
    
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    
    short_description = forms.CharField(max_length=128)
    long_description = forms.CharField(max_length=1024, widget=forms.Textarea)
    
    date_ends = forms.DateField(widget=adminwidgets.AdminDateWidget())
    date_ends.input_formats = [
        '%d/%m/%Y',
        '%d/%m/%y',

        '%d.%m.%Y',
        '%d.%m.%y',

        '%Y-%m-%d',
        '%y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        
        '%d %m %Y',
        '%d %m %y',
    ]
    
    class Meta(object):
        model = Homework
        fields = ('subject', 'short_description', 'long_description', 
            'date_ends',)


class HomeworkCommentForm(forms.ModelForm):
    """Form for creating a comment."""
    
    text = forms.CharField(max_length=2048, widget=forms.Textarea)
    
    class Meta(object):
        model = HomeworkComment
        fields = ('text',)
