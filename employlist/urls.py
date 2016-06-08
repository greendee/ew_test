from django.conf.urls import url
from .views import EmployeeListView


urlpatterns = [
    url(r'^list.html$', EmployeeListView.as_view(), name='list'),
]
