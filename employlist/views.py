from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django import forms
from django.db.models import Q
from django.core.urlresolvers import reverse

from datetime import date
from .models import Employee, Department

# Create your views here.

class FilterForm(forms.Form):
    department = forms.ModelChoiceField(required=False,
                    queryset=Department.objects.all())
    is_employed_now = forms.ChoiceField(choices=(
        ('', 'not set'),
        ('y', 'Yes'),
        ('n', 'No'),
    ), required=False, widget=forms.RadioSelect)

    def get_redirect_url(self):
        if self.is_valid():
            params = {}
            # raw data is passed to reverse() params
            department = self.data.get('department')
            is_employed_now = self.data.get('is_employed_now')

            if department:
                params['department'] = department
            if is_employed_now:
                params['is_employed_now'] = is_employed_now

            return reverse('list2', kwargs=params)
        return reverse('list2')

    def get_queryset_filter(self):
        q = Q()
        if self.is_valid():
            # cleaned data is used in filters
            department = self.cleaned_data.get('department')
            is_employed_now = self.cleaned_data.get('is_employed_now')

            if department:
                q &= Q(department=department)

            if is_employed_now:
                if is_employed_now == 'y':
                    q &= (Q(dismiss_date__isnull=True) |
                          Q(dismiss_date__gte=date.today()))
                else:
                    q &= Q(dismiss_date__lt=date.today())
        return q

class EmployeeListView(ListView):
    model = Employee
    paginate_by = 25
    template_name = 'employlist/list.html'
    context_object_name = 'employees'
    ordering = ['first_name', 'patronymic', 'last_name']

    def apply_queryset_filter(self, queryset):
        form = FilterForm(self.kwargs)
        return queryset.filter(form.get_queryset_filter())

    def get_queryset(self):
        qs = super(EmployeeListView, self).get_queryset()
        return self.apply_queryset_filter(qs)

    def get_context_data(self, **kwargs):
        ctx = super(EmployeeListView, self).get_context_data(**kwargs)
        ctx['form'] = FilterForm(self.kwargs)
        return ctx


class EmployeeFilterView(RedirectView):
    http_method_names = ['get']

    def get_redirect_url(self, *args, **kwargs):
        form = FilterForm(self.request.GET)
        return form.get_redirect_url()
