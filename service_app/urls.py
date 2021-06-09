from django.urls import path
from service_app import views
urlpatterns = [
    path("", views.home, name="home"),
]