from django import forms

from .models import Department


class FilterForm(forms.Form):
    department = forms.ModelChoiceField(required=False,
                    queryset=Department.objects.all())
    is_employed_now = forms.ChoiceField(choices=(
            ('', 'not set'),
            ('y', 'Yes'),
            ('n', 'No'),
        ), required=False, widget=forms.RadioSelect)
