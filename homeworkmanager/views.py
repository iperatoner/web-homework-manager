from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from homeworkmanager.models import Teacher, Subject, Homework, HomeworkComment

def list_all_homework(request):
    pass

def list_subjects_homework(request, subject_name):
    pass

def show_homework(request, subject_name, homework_id):
    pass

def edit_homework(request): # POST data
    pass

def remove_homework(request): # POST data
    pass
