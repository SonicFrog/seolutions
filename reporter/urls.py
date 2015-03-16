from django.conf.urls import patterns, url

from reporter import views

urlpatterns = patterns('',
                       url(r'^$', views.crawl_google_view),
                       url(r'^(?P<site_id>\d+)$', views.crawl_google_view_for_site),
)
