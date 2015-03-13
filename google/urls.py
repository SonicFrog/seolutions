from django.conf.urls import patterns, url

from google import views


urlpatterns = patterns('',
    url(r'^$', views.ReportIndexView.as_view(),
                   name="report-index"),
    url(r'^(?P<pk>\d+)/$', views.ReportDetailView.as_view(),
                name='report-detail'),
    url(r'^(?P<pk>\d+)/delete$', views.ReportDeleteView.as_view(),
                   name="report-delete"),
    url(r'^(?P<first_report_id>\d+)/(?P<second_report_id>\d+)/$',
                   views.ReportCompareView.as_view(), name="report-compare"),

)
