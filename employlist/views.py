from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django import forms
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import Http404
from django.core.paginator import EmptyPage

from datetime import date
from .models import Employee, Department
from math import floor

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


class AlphabeticGroupPaginator(object):

    def __init__(self, queryset, max_pages,
                 orphans=0, allow_empty_first_page=True):
        self.object_list = queryset
        self.max_pages = max_pages
        self.count = self.object_list.count()
        self.pages = []

        letters = {}

        for obj in self.object_list:
            obj_name = unicode(obj)
            letter = obj_name[0]

            if not letters.get(letter):
                letters[letter] = {'count': 0}
            letters[letter]['count'] += 1

        per_page = self.count / float(max_pages)
        count_accum = 0
	letters_sorted = sorted([l for l, d in letters.iteritems()])

        for l in letters_sorted:
            letters[l]['start'] = count_accum
            letters[l]['end'] = count_accum + letters[l]['count']
            letters[l]['mid'] = count_accum + letters[l]['count'] / float(2)
            letters[l]['page'] = int(floor(letters[l]['mid'] / per_page))

            count_accum += letters[l]['count']

        for page in range(0, self.max_pages):
            ltrs = []
            for l in letters_sorted:
                if letters[l]['page'] == page:
                    ltrs.append(letters[l])

            self.pages.append( (ltrs[0]['start'], ltrs[-1]['end']) )


    def page(self, number):
        page = number - 1
        if page in range(self.max_pages):
            return AlphabeticPage(self, \
                     self.object_list[self.pages[page][0]:self.pages[page][1]],
                     number
                   )
        else:
            raise EmptyPage

    def _get_page_range(self):
        return range(1, len(self.pages) + 1)

    page_range = property(_get_page_range)

class AlphabeticPage(object):

    def __init__(self, paginator, object_list, number):
        self.paginator = paginator
        self.object_list = object_list
        self.number = number

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def has_previous(self):
        return self.number > 1

    def has_next(self):
        print self.number
        return len(self.paginator.pages) > self.number

    def next_page_number(self):
        if self.has_next():
            return self.number + 1
        else:
            raise EmptyPage

    def previous_page_number(self):
        if self.has_previous():
            return self.number - 1
        else:
            raise EmptyPage

    def __repr__(self):
        return '<AlphabeticPage (%c-%c)>' % \
            (self.paginator.pages[self.number][0], self.paginator.pages[self.number][1])


class AlphabeticIndexView(ListView):
    model = Employee
    paginate_by = 7
    template_name = 'employlist/alphabetic.html'
    paginator_class = AlphabeticGroupPaginator
    ordering = 'first_name'
    context_object_name = 'employees'

    def get_queryset(self):
        return super(AlphabeticIndexView, self).get_queryset()
