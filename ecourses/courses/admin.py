from django.contrib import admin
from django.template.response import TemplateResponse
from .models import Category, Route, Buses, Tag, Comment, User, Driver, Ticket
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.contrib.auth.models import Group


class RouteAppAdminSite(admin.AdminSite):
        site_header = 'Hệ thống quản lý vé xe khách'

        def get_urls(self):
            return [
                       path('route-stats/', self.stats_view)
                   ] + super().get_urls()

        def stats_view(self, request):
            return TemplateResponse(request,
                                    'admin/route-stats.html')

        def get_app_list(self, request):
                app_list = super().get_app_list(request)
                app_list += [
                        {
                            'name': 'My Custom App',
                            'app_label': 'my_custom_app',
                            'models': [
                                {
                                    'name': 'Statistics',
                                    'object_name': 'route-stats',
                                    'admin_url': '/admin/route-stats',
                                    'view_only': True,
                                }
                            ],
                        }
                    ]
                return app_list




admin.site = RouteAppAdminSite(name='myadmin')




class BusesForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Route
        fields = '__all__'



class BusesInlineAdmin(admin.StackedInline):
    model = Buses
    fk_name = 'route_name' # tên khoá ngoại (tuỳ chọn)



class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'destination', 'name', 'category']
    search_fields = ['name', 'destination']
    list_filter = ['name', 'destination', 'category']
    inlines = [BusesInlineAdmin, ]




class BusesTagInlineAdmin(admin.TabularInline):
    model = Buses.tags.through



class TagAdmin(admin.ModelAdmin):
    inlines = [BusesTagInlineAdmin, ]


class BusesAdmin(admin.ModelAdmin):
    form = BusesForm
    inlines = [BusesTagInlineAdmin, ]
    list_display = ['id', 'name', 'route_name', 'time', 'price', 'seats_status']
    search_fields = ['time', 'name']
    list_filter = ['route_name', 'time', 'seats_status']



class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'successful']
    list_filter = ['id', 'name', 'user', 'successful']
    search_fields = ['name']


admin.site.register(Category)
admin.site.register(Route, RouteAdmin)
admin.site.register(Buses, BusesAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Driver)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Group)