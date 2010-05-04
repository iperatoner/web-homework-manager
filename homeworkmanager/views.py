from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from homeworkmanager.models import Teacher, Subject, Homework, UserProfile
from homeworkmanager.models import HomeworkComment, FinishedHomework

HOMEWORK_ORDER_BY = {
    'ends-soon-first' : 'date_ends',
    'ends-soon-last' : '-date_ends',
    'subject-a-first' : 'subject__name',
    'subject-a-last' : '-subject__name'
}
DEFAULT_ORDER_BY = 'ends-soon-first'

def list_all_homework(request, orderby='ends-soon-first', groupby='subject'):

    if orderby not in HOMEWORK_ORDER_BY:
        orderby = HOMEWORK_ORDER_BY[DEFAULT_ORDER_BY]
    else:
        orderby = HOMEWORK_ORDER_BY[orderby]
        
    homework = Homework.objects.all().order_by(orderby)
        
    data = {
        'homework' : homework,
        'authenticated' : request.user.is_authenticated()
    }
    
    return render_to_response(
        'homeworkmanager/homework-list.html',
        data,
        context_instance = RequestContext(request),
    )
    

def list_subjects_homework(request, subject_name):
    pass

def show_homework(request, subject_name, homework_id):
    pass

def edit_homework(request):
    pass

def remove_homework(request):
    pass

@login_required
def toggle_finished(request):
    try:
        homework_id = int(request.POST['homework_id'])
    except (KeyError, ValueError):
        raise Http404
        
    homework = get_object_or_404(Homework, id=homework_id)
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
    finished_homework, had_to_create = FinishedHomework.objects.get_or_create(user_profile=user_profile, homework=homework)

    if not had_to_create:
        finished_homework.delete()

    return HttpResponseRedirect(reverse('hw_list_all'))
    
