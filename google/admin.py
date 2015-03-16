from django.contrib import admin
from google.models import Site, Report, Keyword, KeywordRelation, User, Responsibility


class KeywordInline(admin.StackedInline):
    model = Site.keywords.through
    extra = 1
    verbose_name = "Keyword"


class UserInline(admin.StackedInline):
    model = Site.admins.through


class SiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['url']}),
    ]

    inlines = [KeywordInline, UserInline]


class KeywordAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Keyword', {'fields': ['keyword']}),
    ]


class ResponbilityAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Person', {'fields': ['person']}),
        ('Website', {'fields': ['site']}),
    ]

    list_display = ('person', 'site')
    list_filter = ['person', 'site']


class KeywordRelAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'site', 'active')
    list_filter = ['keyword', 'site', 'active']


class ReportAdmin(admin.ModelAdmin):
    list_filter = ['site', 'keyword', 'date']
    list_display = ('keyword', 'site', 'date')


admin.site.register(Site, SiteAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Keyword, KeywordAdmin)
