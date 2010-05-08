from django import template

from homeworkmanager.models import UserProfile, FinishedHomework
from homeworkmanager.util import user_finished_homework


def homework_on_main_list(context, homework):
    data = {
        'homework': homework
    }
   
    if context['user'].is_authenticated():
        finished = user_finished_homework(homework, context['user'])
        data.update({
            'finished': finished,
            'orderby' : context['orderby'],
            'authenticated': True,
            'can_edit_homework': context['user'].has_perm('homeworkmanager.change_homework'),
            'can_delete_homework': context['user'].has_perm('homeworkmanager.delete_homework')
        })
    else:
        data['authenticated'] = False

    return data


def show_homework(context, homework):
    data = {
        'homework': homework,
    }
   
    if context['user'].is_authenticated():
        finished = user_finished_homework(homework, context['user'])
        data.update({
            'finished': finished,
            'authenticated': True,
            'can_edit_homework': context['user'].has_perm('homeworkmanager.change_homework'),
            'can_delete_homework': context['user'].has_perm('homeworkmanager.delete_homework')
        })
    else:
        data['authenticated'] = False

    return data

register = template.Library()

register.inclusion_tag(
    'homeworkmanager/templatetags/homework_on_main_list.html',
    takes_context=True
)(homework_on_main_list)

register.inclusion_tag(
    'homeworkmanager/templatetags/show_homework.html',
    takes_context=True
)(show_homework)
