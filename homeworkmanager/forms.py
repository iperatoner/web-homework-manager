from django import forms
from homeworkmanager.models import Homework, Subject

class HomeworkForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    
    short_description = forms.CharField(max_length=128)
    long_description = forms.CharField(max_length=1024, widget=forms.Textarea)
    
    date_ends = forms.DateTimeField()
    date_ends.input_formats = [
        '%d/%m/%Y',
        '%d/%m/%y',

        '%d.%m.%Y',
        '%d.%m.%y',
        
        '%d %m %Y',
        '%d %m %y',
    ]
    
    class Meta(object):
        model = Homework
        fields = ('subject', 'short_description', 'long_description', 'date_ends',)
