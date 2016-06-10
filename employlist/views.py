from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.http import Http404
from django.core.paginator import EmptyPage
from math import floor

from .models import Employee, Department
from .forms import FilterForm
from .helpers import AlphabeticGroupPaginator

# Create your views here.

class EmployeeListView(ListView):
    model = Employee
    paginate_by = 25
    template_name = 'employlist/list.html'
    context_object_name = 'employees'
    ordering = ['first_name', 'patronymic', 'last_name']

    def apply_queryset_filter(self, queryset):
        form = FilterForm(self.kwargs)
        if form.is_valid():
            return queryset.filter(form.get_queryset_filter())
        raise Http404

    def get_queryset(self):
        qs = super(EmployeeListView, self).get_queryset()
        return self.apply_queryset_filter(qs)

    def get_context_data(self, **kwargs):
        ctx = super(EmployeeListView, self).get_context_data(**kwargs)
        form = FilterForm(self.kwargs)
        ctx['form'] = form
        filters = {}
        if form.data.get('department'):
            filters['department'] = form.data.get('department')
        if form.data.get('is_employed_now'):
            filters['is_employed_now'] = form.data.get('is_employed_now')

        ctx['filters'] = filters
        return ctx


class EmployeeFilterView(RedirectView):
    http_method_names = ['get']

    def get_redirect_url(self, *args, **kwargs):
        form = FilterForm(self.request.GET)
        return form.get_redirect_url()


class AlphabeticIndexView(ListView):
    model = Employee
    paginate_by = 7
    template_name = 'employlist/alphabetic.html'
    paginator_class = AlphabeticGroupPaginator
    ordering = 'first_name'
    context_object_name = 'employees'

    def get_queryset(self):
        return super(AlphabeticIndexView, self).get_queryset()
