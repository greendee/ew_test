from __future__ import unicode_literals
from math import floor
from django.db.models import Count
from django.core.paginator import EmptyPage


class AlphabeticGroupPaginator(object):

    def __init__(self, queryset, max_pages,
                 orphans=0, allow_empty_first_page=True):

        self.object_list = queryset
        self.pages = []
        self.page_titles = []

        letter_counts = queryset.model.objects.values_list('first_letter') \
            .annotate(Count('first_letter')).order_by('first_letter')

        total = sum([x[1] for x in letter_counts])
        per_page = total / float(max_pages)
        letter_ranges = {}

        count_accum = 0
        letter_groups = [[] for _ in range(max_pages)]

        for l, c in letter_counts:
            letter_ranges[l] = (count_accum, count_accum + c)

            letter_mid = count_accum + c / 2.0
            page = int(floor(letter_mid / per_page))
            letter_groups[page].append(l)

            count_accum += c

        for n, g in enumerate(letter_groups):
            if len(g) > 0:
                first_letter = g[0]
                last_letter = g[-1]
                start = letter_ranges[first_letter][0]
                end = letter_ranges[last_letter][1]

                self.pages.append([(first_letter, last_letter), (start, end)])
                self.page_titles.append("%c-%c" % (first_letter, last_letter))

    def page(self, number):
        if number in self.page_range:
            page = number - 1
            letter_range = self.pages[page][0]
            start, end = self.pages[page][1]

            return AlphabeticPage(self, \
                        self.object_list[start:end], number)
        else:
            raise EmptyPage

    def _get_page_range(self):
        return range(1, len(self.pages) + 1)

    page_range = property(_get_page_range)

    def _get_pages_with_title(self):
        return [(n, self.page_titles[n - 1]) for n in self.page_range]

    pages_with_title = property(_get_pages_with_title)


class AlphabeticPage(object):

    def __init__(self, paginator, object_list, number):
        self.paginator = paginator
        self.object_list = object_list
        self.number = number
        self.letter_range = paginator.page_titles[number - 1]

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def has_previous(self):
        return self.number > 1

    def has_next(self):
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
        return '<AlphabeticPage (%s)>' % (self.letter_range)
