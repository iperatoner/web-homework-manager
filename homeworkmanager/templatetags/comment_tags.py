from django import template

from homeworkmanager.models import HomeworkComment
from homeworkmanager.util import user_finished_homework


def show_homework_comments(context, homework):
    data = {
        'homework': homework,
        'comments': homework.comment_set.all(),
        'authenticated': context['user'].is_authenticated()
    }

    return data
    

def show_single_comment(context, comment):
    finished = user_finished_homework(comment.homework, comment.user)
    
    data = {
        'comment': comment,
        'finished_related_homework': finished
    }

    return data

register = template.Library()

register.inclusion_tag(
    'homeworkmanager/templatetags/show_homework_comments.html',
    takes_context=True
)(show_homework_comments)

register.inclusion_tag(
    'homeworkmanager/templatetags/show_single_comment.html',
    takes_context=True
)(show_single_comment)
