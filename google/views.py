from django.views import generic
from django.http import Http404

from google.models import Report, Site, Keyword


class LoggedInMixin:
    """
    Mixed used to disallow anonymous access to views
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)


class SiteIndexView(generic.ListView, LoggedInMixin):
    """
    Displays all the sites the current user is an admin for
    """
    template_name = 'sites/list.html'
    context_object_name = 'site_list'

    def get_queryset(self):
        q = Site.objects.filter(admins=self.request.user)
        return q


class SiteDetailView(generic.DetailView, LoggedInMixin):
    """
    Displays details for a given sites, including the last few reports
    for this site.
    """
    template_name = 'sites/detail.html'
    model = Site

    def get_object(self, queryset=None):
        site = super(SiteDetailView, self).get_object()
        if self.request.user not in site.admins:
            raise Http404
        return site

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        site = self.get_object()
        context['report_list'] = Report.objects.filter(
            site__pk=site.pk).order_by('date').reverse()
        return context


class ReportIndexView(generic.ListView, LoggedInMixin):
    """
    Displays an index of reports for the sites the person is responsible
    """
    template_name = 'reports/index.html'
    context_object_name = 'latest_report_list'

    def get_queryset(self):
        r = Report.objects.filter(site__admins=self.request.user)
        return r.order_by('date')[:5]


class ReportDetailView(generic.DetailView, LoggedInMixin):
    """
    Displays details for a given report provided the logged user
    is an administrator for the site the report belongs to.
    """
    model = Report
    context_object_name = 'report'
    template_name = 'reports/detail.html'

    def get_object(self, queryset=None):
        report = super(ReportDetailView, self).get_object()
        if self.request.user not in report.site.admins:
            raise Http404
        return report


class ReportDeleteView(generic.DeleteView, LoggedInMixin):
    template_name = 'reports/delete.html'
    context_object_name = 'report'
    model = Report

    success_url = "/"

    def get_object(self, queryset=None):
        """
        Checking the current user is an administrator of the site this
        report belongs to before performing the deletion
        """
        obj = super(generic.DeleteView, self).get_object()
        if self.request.user not in obj.site.admins:
            raise Http404
        else:
            return obj


class ReportCompareView(generic.View, LoggedInMixin):
    template_name = 'reports/compare.html'

    def get_context_data(self, **kwargs):
        context = super(ReportCompareView, self).get_context_data(**kwargs)
        id_1, id_2 = kwargs['first_report_id'], kwargs['second_report_id']
        context['report_1'] = Report.objects.get(pk=id_1)
        context['report_2'] = Report.objects.get(pk=id_2)
        return context


class ReportCreateView(generic.TemplateView, LoggedInMixin):
    template_name = "reports/create.html"


class KeywordIndexView(generic.ListView, LoggedInMixin):
    template_name = 'reports/bykw.html'
    model = Keyword
    context_object_name = 'keyword_list'

    def get_queryset(self, **kwargs):
        return Keyword.objects.filter(
            site__admins=self.request.user).order_by('keyword')
