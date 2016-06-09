from django.conf.urls import url
from django.views.generic import DetailView
from .views import EmployeeListView
from .models import Employee

urlpatterns = [
    url(r'^employees/$', EmployeeListView.as_view(), name='list'),
    url(r'^employees/(?P<pk>[0-9]+).html',
        DetailView.as_view(
            model=Employee, template_name='employlist/detail.html',
            context_object_name='employee'
        ),
        name='detail'
    ),
]
