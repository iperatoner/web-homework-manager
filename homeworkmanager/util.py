from django.shortcuts import get_object_or_404
from django.http import Http404

from homeworkmanager.models import Homework, FinishedHomework, UserProfile

def get_homework_or_404(subject_name, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    
    if homework.subject.name != subject_name:
        raise Http404('Given Homework subject "%s" did not match homework with ID %s.' % 
            (subject_name, homework_id))
        
    return homework
    

def user_finished_homework(homework, user):
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    try:
        FinishedHomework.objects.get(user_profile=user_profile, homework=homework)
        finished = True
    except FinishedHomework.DoesNotExist:
        finished = False
        
    return finished
