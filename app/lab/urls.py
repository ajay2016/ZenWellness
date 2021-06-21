from django.urls import path
from .views import Dashboard, TestList

app_name = 'lab'

urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard"),
    path('tests/', TestList.as_view(), name="tests_list"),
]
