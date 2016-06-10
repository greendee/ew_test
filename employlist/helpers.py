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
