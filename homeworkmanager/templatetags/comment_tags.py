from django import template

from homeworkmanager.models import HomeworkComment
from homeworkmanager.util import user_finished_homework

register = template.Library()

@register.inclusion_tag(
    'homeworkmanager/templatetags/show_homework_comments.html',
    takes_context=True
)
def show_homework_comments(context, homework):
    """This inclusion tag displays all comments
    related to the given homework."""
    
    data = {
        'homework': homework,
        'comments': homework.comment_set.all()
    }

    context.update(data)
    
    return context

    
@register.inclusion_tag(
    'homeworkmanager/templatetags/show_single_comment.html',
    takes_context=True
)
def show_single_comment(context, comment):
    """This inclusion tag displays a single comment."""
    
    finished = user_finished_homework(comment.homework, comment.user)
    
    data = {
        'comment': comment,
        'finished_related_homework': finished
    }
    
    context.update(data)

    return context
