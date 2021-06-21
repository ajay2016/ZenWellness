from django.urls import path
from .views import (
    LandingView, MedicineView, Login, Logout, Dashboard
)

app_name = 'website'

urlpatterns = [
    path('', LandingView.as_view(), name="landing"),
    path('auth/login/', Login.as_view(), name="login"),
    path('auth/logout/', Logout.as_view(), name="logout"),
    path('medicines/', MedicineView.as_view(), name="medicine"),
    path('dashboard/', Dashboard.as_view(), name="dashboard")
]
