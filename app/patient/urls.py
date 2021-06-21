from django.urls import path
from .views import Dashboard, Profile

app_name = 'patient'

urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard"),
    path('profile/', Profile.as_view(), name="profile")
]
