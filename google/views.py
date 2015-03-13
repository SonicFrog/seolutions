from django.views import generic
from django.http import Http404

from google.models import Report
from users.views import LoginRequiredMixin


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
    pass


class ReportCreateView(generic.TemplateView, LoginRequiredMixin):
    template_name = "reports/create.html"
