from django.views import generic
from django.http import Http404

from google.models import Report, Site, KeywordRelation, Keyword
from users.views import LoginRequiredMixin


class SiteIndexView(generic.ListView, LoginRequiredMixin):
    template_name = 'sites/list.html'
    context_object_name = 'site_list'

    def get_queryset(self):
        return Site.objects.order_by('name')


class SiteDetailView(generic.DetailView, LoginRequiredMixin):
    template_name = 'sites/detail.html'
    model = Site

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['report_list'] = Report.objects.filter(
            site=kwargs['object'].pk).order_by('date').reverse()
        return context


class ReportIndexView(generic.ListView, LoginRequiredMixin):
    template_name = 'reports/index.html'
    context_object_name = 'latest_report_list'

    def get_queryset(self):
        return Report.objects.order_by('date')[:5]


class ReportDetailView(generic.DetailView, LoginRequiredMixin):
    model = Report
    context_object_name = 'report'
    template_name = 'reports/detail.html'


class ReportDeleteView(generic.DeleteView, LoginRequiredMixin):
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


class ReportCompareView(generic.View, LoginRequiredMixin):
    template_name = 'reports/compare.html'

    def get_context_data(self, **kwargs):
        pass


class ReportCreateView(generic.TemplateView, LoginRequiredMixin):
    template_name = "reports/create.html"


class KeywordIndexView(generic.ListView, LoginRequiredMixin):
    template_name = 'reports/bykw.html'
    model = Keyword
    context_object_name = 'keyword_list'

    def get_queryset(self, **kwargs):
        return Keyword.objects.all().order_by('keyword')
