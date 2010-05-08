from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext

from homeworkmanager.models import Teacher, Subject, Homework, UserProfile
from homeworkmanager.models import HomeworkComment, FinishedHomework
from homeworkmanager.forms import HomeworkForm, HomeworkCommentForm
from homeworkmanager.util import get_homework_or_404

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
        'authenticated' : request.user.is_authenticated(),
        'can_add_homework' : request.user.has_perm('homeworkmanager.add_homework')
    }
    
    return render_to_response(
        'homeworkmanager/homework-list.html',
        data,
        context_instance = RequestContext(request),
    )
    

def show_homework(request, subject_name, homework_id, form=False):
    homework = get_homework_or_404(subject_name, homework_id)
        
    if not form:
        form = HomeworkCommentForm()
        
    data = {
        'homework': homework,
        'form': form,
        'authenticated': request.user.is_authenticated()
    }

    return render_to_response(
        'homeworkmanager/show.html',
        data,
        context_instance = RequestContext(request),
    )


@permission_required('homeworkmanager.add_homework')
def create_homework(request):
    form = HomeworkForm(request.POST or None)

    if form.is_valid():
        homework = form.save()
        request.user.message_set.create(message="Homework was created.")
        return HttpResponseRedirect(reverse('hw_list_all'))

    data = {
        'form': form,
        'new' : True,
        'homework': None
    }

    return render_to_response(
        'homeworkmanager/edit.html',
        data,
        context_instance = RequestContext(request),
    )


@permission_required('homeworkmanager.change_homework')
def edit_homework(request, subject_name, homework_id):
    homework = get_homework_or_404(subject_name, homework_id)
    
    if 'next' in request.GET.keys():
        next = request.GET['next']
    else:
        next = False
    
    if not request.POST:
        form = HomeworkForm(instance=homework)
    else:
        form = HomeworkForm(request.POST)
        
        if form.is_valid():
            homework.short_description = form.cleaned_data['short_description']
            homework.long_description = form.cleaned_data['long_description']
            homework.date_ends = form.cleaned_data['date_ends']
            homework.subject = form.cleaned_data['subject']
            
            homework.save()
            
            request.user.message_set.create(message="Your homework was saved.")
            
            if next:
                return HttpResponseRedirect(reverse(next, args=[homework.subject.name, homework.id]))
            else:
                return HttpResponseRedirect(reverse('hw_list_all'))

    data = {
        'form': form,
        'new': False,
        'homework': homework,
        'next': next
    }

    return render_to_response(
        'homeworkmanager/edit.html',
        data,
        context_instance = RequestContext(request),
    )


@permission_required('homeworkmanager.delete_homework')  
def remove_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    homework.delete()
    
    request.user.message_set.create(message="The homework was removed.")
    
    try:
        if 'orderby' in request.POST.keys() and request.POST['orderby'] != DEFAULT_ORDER_BY:
            next = reverse('hw_list_all_sorted', args=[request.POST['orderby']])
        else:
            next = reverse('hw_list_all')
    except KeyError:
        raise Http404
        
    return HttpResponseRedirect(next)


@login_required
def toggle_finished(request, homework_id):        
    homework = get_object_or_404(Homework, id=homework_id)
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
    finished_homework, had_to_create = FinishedHomework.objects.get_or_create(
        user_profile=user_profile, homework=homework)

    if not had_to_create:
        finished_homework.delete()
        
    try:
        if 'show_homework' not in request.POST.keys():
            if request.POST['orderby'] != DEFAULT_ORDER_BY:
                next = reverse('hw_list_all_sorted', args=[request.POST['orderby']])
            else:
                next = reverse('hw_list_all')
        else:
            next = reverse('hw_show', args=[homework.subject.name, homework.id])
    except KeyError:
        raise Http404
        
    return HttpResponseRedirect(next)
    

@login_required
def add_comment(request, subject_name, homework_id):
    homework = get_homework_or_404(subject_name, homework_id)
    
    form = HomeworkCommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.homework = homework
        comment.save()
        
        request.user.message_set.create(message="Comment was created.")
        
        return HttpResponseRedirect(
            reverse('hw_show', args=[
                subject_name,
                homework_id
            ]) + '#comments'
        )
    
    return show_homework(request, subject_name, homework_id, form)
