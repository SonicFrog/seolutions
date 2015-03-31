from django.views import generic
from django.http import Http404, HttpResponseForbidden

from google.models import Report, Site, Keyword


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)


class SiteIndexView(generic.ListView, LoggedInMixin):
    template_name = 'sites/list.html'
    context_object_name = 'site_list'

    def get_queryset(self):
        q = Site.objects.filter(admins=self.request.user)
        return q


class SiteDetailView(generic.DetailView, LoggedInMixin):
    template_name = 'sites/detail.html'
    model = Site

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['report_list'] = Report.objects.filter(
            site=kwargs['object'].pk).order_by('date').reverse()
        return context


class ReportIndexView(generic.ListView, LoggedInMixin):
    template_name = 'reports/index.html'
    context_object_name = 'latest_report_list'

    def get_queryset(self):
        r = Report.objects.filter(site__admins=self.request.user)
        return r.order_by('date')[:5]


class ReportDetailView(generic.DetailView, LoggedInMixin):
    model = Report
    context_object_name = 'report'
    template_name = 'reports/detail.html'

    def get_queryset(self):
        return Report.objects.filter(site__admins=self.request.user)


class ReportDeleteView(generic.DeleteView, LoggedInMixin):
    template_name = 'reports/delete.html'
    context_object_name = 'report'
    model = Report

    success_url = "/"

    def get_object(self, queryset=None):
        """
        Checking the current user is an administrator of the site this
        report is about before performing the deletion
        """
        obj = super(generic.DeleteView, self).get_object()
        if self.request.user not in obj.site.admins.all():
            raise Http404
        else:
            return obj


class ReportCompareView(generic.View, LoggedInMixin):
    template_name = 'reports/compare.html'

    def get_context_data(self, **kwargs):
        pass


class ReportCreateView(generic.TemplateView, LoggedInMixin):
    template_name = "reports/create.html"


class KeywordIndexView(generic.ListView, LoggedInMixin):
    template_name = 'reports/bykw.html'
    model = Keyword
    context_object_name = 'keyword_list'

    def get_queryset(self, **kwargs):
        return Keyword.objects.all().order_by('keyword')
