from django.shortcuts import get_object_or_404
from django.http import Http404

from homeworkmanager.models import Homework, FinishedHomework, UserProfile

def get_homework_or_404(subject_name, homework_id):
    """This function checks if a homework matches the given
    subject name and homework id and returns a proper Http response."""
    
    homework = get_object_or_404(Homework, id=homework_id)
    
    # Check if the subject name of the homework matches the given subject name
    if homework.subject.name != subject_name:
        raise Http404(
            'Given Homework subject "%s" did not match homework with ID %s.' % 
            (subject_name, homework_id))
        
    return homework
    

def user_finished_homework(homework, user):
    """This function checks wether the given user has already finished the
    given homework."""
    
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    try:
        FinishedHomework.objects.get(user_profile=user_profile,
            homework=homework)
        finished = True
    except FinishedHomework.DoesNotExist:
        finished = False
        
    return finished
