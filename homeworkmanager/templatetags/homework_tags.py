from django import template

from homeworkmanager.models import UserProfile, FinishedHomework
from homeworkmanager.util import user_finished_homework

register = template.Library()

@register.inclusion_tag(
    'homeworkmanager/templatetags/homework_on_main_list.html',
    takes_context=True
)
def homework_on_main_list(context, homework):
    """This inclusion tag shows a single homework on the main homework list."""
    data = {
        'homework': homework
    }
   
    if context['user'].is_authenticated():
        finished = user_finished_homework(homework, context['user'])
        data['finished'] = finished
    
    context.update(data)
    
    return context


@register.inclusion_tag(
    'homeworkmanager/templatetags/show_homework.html',
    takes_context=True
)
def show_homework(context, homework):
    """This inclusion tag shows a single homework and all its data."""
    
    data = {
        'homework': homework,
    }
   
    if context['user'].is_authenticated():
        finished = user_finished_homework(homework, context['user'])
        data['finished'] = finished
        
    context.update(data)

    return context
