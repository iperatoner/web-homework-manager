from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission

from django.template import RequestContext

from homeworkmanager.models import Teacher, Subject, Homework, UserProfile
from homeworkmanager.models import HomeworkComment, FinishedHomework
from homeworkmanager.forms import HomeworkForm, HomeworkCommentForm
from homeworkmanager.forms import UserRegistrationForm
from homeworkmanager.util import get_homework_or_404

# Ordering possibilities
HOMEWORK_ORDER_BY = {
    'ends-soon-first' : 'date_ends',
    'ends-soon-last' : '-date_ends',
    'az' : 'subject__name',
    'za' : '-subject__name'
}
DEFAULT_ORDER_BY = 'ends-soon-first'

def list_all_homework(request, orderby='ends-soon-first', groupby='subject'):
    """This view lists all available homework in a specific order."""
    
    # Choose the correct ordering type
    if orderby not in HOMEWORK_ORDER_BY:
        model_orderby = HOMEWORK_ORDER_BY[DEFAULT_ORDER_BY]
    else:
        model_orderby = HOMEWORK_ORDER_BY[orderby]
        
    homework = Homework.objects.all().order_by(model_orderby)
        
    data = {
        'homework' : homework,
        'orderby' : orderby,
        'can_add_homework' : request.user.has_perm(
            'homeworkmanager.add_homework'),
    }
    
    return render_to_response(
        'homeworkmanager/homework-list.html',
        data,
        context_instance = RequestContext(request),
    )
    

def show_homework(request, subject_name, homework_id, form=False):
    """This view shows a single homework and all its comments."""
    
    homework = get_homework_or_404(subject_name, homework_id)
    
    # Create a comment form if it's not given (via the `add_comment` view)
    if not form:
        form = HomeworkCommentForm()
        
        
    data = {
        'homework': homework,
        'form': form
    }

    return render_to_response(
        'homeworkmanager/show.html',
        data,
        context_instance = RequestContext(request),
    )


@permission_required('homeworkmanager.add_homework')
def create_homework(request):
    """
    This view displays a form for creating a homework resp. 
    creates a homework using the form data.
    """
    
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
    """
    This view displays a form to edit a homework resp.
    saves a homework using the form data.
    """
    
    homework = get_homework_or_404(subject_name, homework_id)
    
    # Check if a `next_view` was specified in POST data 
    # (e.g. when clicking "edit" from a single displayed homework)
    if 'next_view' in request.POST.keys():
        next_view = request.POST['next_view']
    else:
        next_view = False
    
    if not request.POST or len(request.POST) == 3:
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
            
            if next_view:
                return HttpResponseRedirect(reverse(next_view, 
                    args=[homework.subject.name, homework.id]))
            else:
                return HttpResponseRedirect(reverse('hw_list_all'))

    data = {
        'form': form,
        'new': False,
        'homework': homework,
        'next_view': next_view
    }

    return render_to_response(
        'homeworkmanager/edit.html',
        data,
        context_instance = RequestContext(request),
    )


@permission_required('homeworkmanager.delete_homework')  
def remove_homework(request, homework_id):
    """This view removes a homework by the given homework id."""
    
    homework = get_object_or_404(Homework, id=homework_id)
    homework.delete()
    
    request.user.message_set.create(message="The homework was removed.")
    
    try:
        # If the remove button was pressed on the main homework list
        # we have to check if the user has specified a different order
        if 'orderby' in request.POST.keys() and \
            request.POST['orderby'] != DEFAULT_ORDER_BY:
            
            next = reverse('hw_list_all_sorted', 
                args=[request.POST['orderby']])
        else:
            next = reverse('hw_list_all')
    except KeyError:
        raise Http404
        
    return HttpResponseRedirect(next)


@login_required
def toggle_finished(request, homework_id):   
    """
    This view toggles a homework for the currently 
    logged in user as finished/unfinished.
    """
    
    homework = get_object_or_404(Homework, id=homework_id)
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
    finished_homework, had_to_create = FinishedHomework.objects.get_or_create(
        user_profile=user_profile, homework=homework)

    if not had_to_create:
        finished_homework.delete()
        
    try:
        # If the homework was toggled as finished/unfinished from the main list
        # we have to check the specified ordering
        if 'show_homework' not in request.POST.keys():
            if request.POST['orderby'] != DEFAULT_ORDER_BY:
                next = reverse('hw_list_all_sorted',
                    args=[request.POST['orderby']])
            else:
                next = reverse('hw_list_all')
        else:
            next = reverse('hw_show',
                args=[homework.subject.name, homework.id])
    except KeyError:
        raise Http404
        
    return HttpResponseRedirect(next)
    

@login_required
def add_comment(request, subject_name, homework_id):
    """This view creates a comment on the given homework (subject name, id)."""
    
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
    

def login(request):
    """This view logs a user in resp. displays a form for logging in."""
    
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('hw_list_all'))
        
    invalid_login = False
    account_disabled = False
    
    # Check if a redirect url has been specified
    if 'next' in request.GET.keys():
        next = request.GET['next']
    elif 'next' in request.POST.keys():
        next = request.POST['next']
    else:
        next = False
    
    if request.POST:
        user = django_authenticate(username=request.POST['username'],
            password=request.POST['password'])
        if user is not None:
            if user.is_active:
                django_login(request, user)
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(reverse('hw_list_all'))
            else:
                account_disabled = True
        else:
            invalid_login = True
        
    data = {
        'invalid_login': invalid_login,
        'account_disabled': account_disabled,
        'next' : next
    }
        
    return render_to_response(
        'homeworkmanager/login.html',
        data,
        context_instance = RequestContext(request),
    )
    

def logout(request):
    """This view just logs the currently logged in user out."""
    
    django_logout(request)
    return HttpResponseRedirect(reverse('hw_list_all'))


def register(request):
    """This view registers a new users resp. displays a form to do so."""
    
    if not request.POST:
        form = UserRegistrationForm()
    else:
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email = form.cleaned_data['email']
            user.save()
            
            # Adding default permissions
            perms = Permission.objects.filter(
                codename__in=['add_homework', 'change_homework']
            )
            user.user_permissions.add(perms[0], perms[1])
            user.save()
            
            # Notification email
            email_subject = 'Registrierung auf fg09b.de'
            email_body = """Hallo %s,
            
du hast dich auf fg09b.de registriert. Bevor du deinen Account nutzen kannst,
muss ein Administrator dich freischalten.

Benutzername: %s
Passwort: %s

lg, fg09b.de hausaufgabensystem""" % (user.username, user.username, form.cleaned_data['password1'])
            
            email_subject_cc = 'Neuer Benutzer auf FG09B.de'
            email_body_cc = """Auf fg09b.de hat sich ein neuer Benutzer registriert.
            
-------------------------------------------------------------

            """ + email_body
            
            email_from = 'fg09b-registrierung@fg09b.de'
            
            send_mail(email_subject, email_body, email_from, [user.email])
            send_mail(email_subject_cc, email_body_cc, email_from, ['immanuel.peratoner@gmail.com'])
            
            return HttpResponseRedirect(reverse('hw_list_all'))
        
    data = {
        'form': form,
    }
        
    return render_to_response(
        'homeworkmanager/register.html',
        data,
        context_instance = RequestContext(request),
    )

