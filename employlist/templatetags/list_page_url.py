from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.simple_tag(takes_context=True)
def list_page_url(context, page):
    params = {}
    if context['filters'].get('department'):
        params['department'] = context['filters'].get('department')
    if context['filters'].get('is_employed_now'):
        params['is_employed_now'] = context['filters'].get('is_employed_now')
    params['page'] = page

    return reverse('list', kwargs=params)
