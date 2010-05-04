from django.conf.urls.defaults import *
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('homeworkmanager.urls')),
    (r'^admin/', include(admin.site.urls)),
)
