from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.http import Http404
from django.core.urlresolvers import reverse
from django.db.models import Q

from datetime import date

from .models import Employee, Department
from .forms import FilterForm
from .helpers import AlphabeticGroupPaginator

# Create your views here.

class EmployeeListView(ListView):
    model = Employee
    paginate_by = 25
    template_name = 'employlist/list.html'
    context_object_name = 'employees'
    ordering = ['last_name', 'first_name', 'patronymic']
    allow_empty = False

    def apply_queryset_filter(self, queryset):
        form = FilterForm(self.kwargs)
        if form.is_valid():
            q = Q()

            # cleaned data is used in filters
            department = form.cleaned_data.get('department')
            is_employed_now = form.cleaned_data.get('is_employed_now')

            if department:
                q &= Q(department=department)

            if is_employed_now:
                if is_employed_now == 'y':
                    q &= (Q(dismiss_date__isnull=True) |
                          Q(dismiss_date__gte=date.today()))
                else:
                    q &= Q(dismiss_date__lt=date.today())

            return queryset.filter(q)

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
        if form.is_valid():
            params = {}
            # raw data is passed to reverse() params
            department = self.data.get('department')
            is_employed_now = self.data.get('is_employed_now')

            if department:
                params['department'] = department
            if is_employed_now:
                params['is_employed_now'] = is_employed_now

            return reverse('list', kwargs=params)

        return reverse('list')


class AlphabeticIndexView(ListView):
    model = Employee
    paginate_by = 7
    template_name = 'employlist/alphabetic.html'
    paginator_class = AlphabeticGroupPaginator
    ordering = 'last_name'
    context_object_name = 'employees'

    def get_queryset(self):
        return super(AlphabeticIndexView, self).get_queryset()
