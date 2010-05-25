from django.conf.urls.defaults import *
from homeworkmanager import views

urlpatterns = patterns('',
    url(
        r'^sort/(?P<orderby>.+)/$',
        views.list_all_homework,
        name='hw_list_all_sorted'
    ),
    url(
        r'^toggle-finished/(?P<homework_id>[0-9]+)/$',
        views.toggle_finished,
        name='hw_toggle_finished'
    ),
    url(
        r'^show/(?P<subject_name>[a-zA-Z0-9_-]+)/(?P<homework_id>[0-9]+)/$',
        views.show_homework,
        name='hw_show'
    ),
    url(
        r'^show/(?P<subject_name>[a-zA-Z0-9_-]+)/(?P<homework_id>[0-9]+)/add-comment/$',
        views.add_comment,
        name='hw_add_comment'
    ),
    url(
        r'^create/$',
        views.create_homework,
        name='hw_create'
    ),
    url(
        r'^edit/(?P<subject_name>[a-zA-Z0-9_-]+)/(?P<homework_id>[0-9]+)/$',
        views.edit_homework,
        name='hw_edit'
    ),
    url(
        r'^remove/(?P<homework_id>[0-9]+)/$',
        views.remove_homework,
        name='hw_remove'
    ),
    url(
        r'^login/$',
        views.login,
        name='hw_login'
    ),
    url(
        r'^logout/$',
        views.logout,
        name='hw_logout'
    ),
    url(r'^$', views.list_all_homework, name='hw_list_all'),
)
