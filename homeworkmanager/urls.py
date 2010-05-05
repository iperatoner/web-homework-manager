from django.conf.urls.defaults import *
from homeworkmanager import views

urlpatterns = patterns('',
    url(
        r'^sort/(?P<orderby>.+)/$',
        views.list_all_homework,
        name='hw_list_all_sorted'
    ),
    url(
        r'^toggle-finished/$',
        views.toggle_finished,
        name='hw_toggle_finished'
    ),
    url(
        r'^edit/(?P<subject_name>[a-zA-Z0-9_-]+)/(?P<homework_id>[0-9]+)/$',
        views.edit_homework,
        name='hw_edit'
    ),
    url(
        r'^edit/$',
        views.edit_homework,
        name='hw_create'
    ),
    url(r'^$', views.list_all_homework, name='hw_list_all'),
)
