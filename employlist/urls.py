from django.conf.urls import url
from django.views.generic import DetailView
from .views import EmployeeListView, EmployeeFilterView
from .models import Employee

urlpatterns = [
    url(r'^employees/' \
            + r'(?:dep-(?P<department>[0-9]+)/)?' \
            + r'(?:emp-(?P<is_employed_now>(y|n)+)/)?' \
            + r'(?:page-(?P<page>[0-9]+)/)?' \
            + r'$',
        EmployeeListView.as_view(), name='list2'
    ),
    url(r'^employees/apply-filter/',
        EmployeeFilterView.as_view(), name='filter'
    ),
    url(r'^employees/(?P<pk>[0-9]+).html',
        DetailView.as_view(
            model=Employee, template_name='employlist/detail.html',
            context_object_name='employee'
        ), name='detail'
    ),
]
