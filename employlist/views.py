from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django import forms
from django.db.models import Q

from datetime import date
from .models import Employee, Department

# Create your views here.

class FilterForm(forms.Form):
    department = forms.ModelChoiceField(required=False,
                     queryset=Department.objects.all())
    is_employed_now = forms.NullBooleanField(required=False)


class EmployeeListView(FormMixin, ListView):
    model = Employee
    paginate_by = 25
    template_name = 'employlist/list.html'
    context_object_name = 'employees'

    form_class = FilterForm

    def get_form(self):
        return FilterForm(self.request.GET)

    def apply_queryset_filter(self, queryset):
        form = self.get_form()

        if form.is_valid():
            department = form.cleaned_data['department']
            is_employed_now = form.cleaned_data['is_employed_now']

            if department is not None:
                queryset = queryset.filter(department=department)

            if is_employed_now is not None:
                if is_employed_now:
                    queryset = queryset.filter( Q(dismiss_date__isnull=True) |
                                   Q(dismiss_date__gte=date.today()) )
                else:
                    queryset = queryset.filter(dismiss_date__lt=date.today())

        return queryset


    def get_queryset(self):
        qs = super(EmployeeListView, self).get_queryset()
        return self.apply_queryset_filter(qs)
