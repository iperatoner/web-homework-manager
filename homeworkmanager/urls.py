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
    url(r'^$', views.list_all_homework, name='hw_list_all'),
)
