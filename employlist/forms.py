from django import forms
from django.db.models import Q
from django.core.urlresolvers import reverse
from datetime import date


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

            return reverse('list', kwargs=params)
        return reverse('list')

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
