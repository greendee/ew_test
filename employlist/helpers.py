from __future__ import unicode_literals
from math import floor


class AlphabeticGroupPaginator(object):

    def __init__(self, queryset, max_pages,
                 orphans=0, allow_empty_first_page=True):
        self.object_list = queryset
        self.max_pages = max_pages
        self.count = self.object_list.count()
        self.pages = []

        self.letters = {}

        for obj in self.object_list:
            obj_name = unicode(obj)
            letter = obj_name[0]

            if not self.letters.get(letter):
                self.letters[letter] = {'count': 0}
            self.letters[letter]['count'] += 1

        per_page = self.count / float(max_pages)
        count_accum = 0
	letters_sorted = sorted([l for l, d in self.letters.iteritems()])

        for l in letters_sorted:
            self.letters[l]['start'] = count_accum
            self.letters[l]['end'] = \
                count_accum + self.letters[l]['count']
            self.letters[l]['mid'] = \
                count_accum + self.letters[l]['count'] / float(2)
            self.letters[l]['page'] = \
                int(floor(self.letters[l]['mid'] / per_page))

            count_accum += self.letters[l]['count']

        for page in range(0, self.max_pages):
            ltrs = []
            for l in letters_sorted:
                if self.letters[l]['page'] == page:
                    ltrs.append(l)

            self.pages.append( (ltrs[0], ltrs[-1]) )
            print(self.pages[page])


    def page(self, number):
        page = number - 1
        if page in range(self.max_pages):
            return AlphabeticPage(self, \
                     self.object_list[
                         self.letters[self.pages[page][0]]['start']: \
                         self.letters[self.pages[page][1]]['end']
                     ],
                     number
                   )
        else:
            raise EmptyPage

    def _get_page_range(self):
        return xrange(1, len(self.pages) + 1)

    page_range = property(_get_page_range)

class AlphabeticPage(object):

    def __init__(self, paginator, object_list, number):
        self.paginator = paginator
        self.object_list = object_list
        self.number = number
        self.letter_range = '%c-%c' % \
                (self.paginator.pages[self.number - 1][0],
                 self.paginator.pages[self.number - 1][1])

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
        return '<AlphabeticPage (%s)>' % (self.letter_range)
