from homeworkmanager.models import UserProfile, FinishedHomework
from django import template

def homework_on_main_list(context, homework):
    data = {
        'homework': homework,
    }
   
    if context['user'].is_authenticated():
        try:
            user_profile = UserProfile.objects.get_or_create(user=context['user'])[0]
            FinishedHomework.objects.get(user_profile=user_profile, homework=homework)
            finished = True
        except FinishedHomework.DoesNotExist:
            finished = False
        
        data.update({
            'finished': finished,
            'authenticated': True,
        })
    else:
        data['authenticated'] = False

    return data

register = template.Library()
register.inclusion_tag('homeworkmanager/templatetags/homework_on_main_list.html', takes_context=True)(homework_on_main_list)
