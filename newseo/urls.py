from django.conf.urls import patterns, include, url
from django.contrib import admin

from google import views
from users import views

urlpatterns = patterns('',
                       url(r'^patateries/', include(admin.site.urls)),
                       url(r'^reports/', include('google.urls')),
                       url(r'^login/', include('users.urls')),
                       url(r'^create/', include('reporter.urls')),
)
