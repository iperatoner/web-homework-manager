from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from homeworkmanager.models import Teacher, Subject, Homework, UserProfile
from homeworkmanager.models import HomeworkComment, FinishedHomework
from homeworkmanager.forms import HomeworkForm

HOMEWORK_ORDER_BY = {
    'ends-soon-first' : 'date_ends',
    'ends-soon-last' : '-date_ends',
    'az' : 'subject__name',
    'za' : '-subject__name'
}
DEFAULT_ORDER_BY = 'ends-soon-first'

def list_all_homework(request, orderby='ends-soon-first', groupby='subject'):

    if orderby not in HOMEWORK_ORDER_BY:
        model_orderby = HOMEWORK_ORDER_BY[DEFAULT_ORDER_BY]
    else:
        model_orderby = HOMEWORK_ORDER_BY[orderby]
        
    homework = Homework.objects.all().order_by(model_orderby)
        
    data = {
        'homework' : homework,
        'orderby' : orderby,
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


@login_required
def edit_homework(request, subject_name=False, homework_id=False):
    if subject_name and homework_id:
        homework = get_object_or_404(Homework, id=homework_id)
        
        if homework.subject.name != subject_name:
            raise Http404
            
        form = HomeworkForm(instance=homework)
        exists = True
    else:
        form = HomeworkForm(request.POST or None)
        exists = False

    if form.is_valid() and not exists:
        homework = form.save()
        request.user.message_set.create(message="Your event was posted.")
        return HttpResponseRedirect(reverse('hw_list_all'))

    data = {
        'form': form,
        'exists': exists
    }

    return render_to_response(
        'homeworkmanager/edit.html',
        data,
        context_instance = RequestContext(request),
    )

    
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
        
    try:
        if request.POST['orderby'] == DEFAULT_ORDER_BY:
            next = reverse('hw_list_all')
        else:
            next = reverse('hw_list_all_sorted', args=[request.POST['orderby']])
    except KeyError:
        raise Http404
        
    return HttpResponseRedirect(next)
    
