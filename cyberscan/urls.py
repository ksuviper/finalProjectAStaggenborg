from django.urls import path, include
from . import views

app_name = "cyberscan"
urlpatterns = [
    path("", views.index, name="index"),
    path("trace/", views.trace, name="trace"),
    path("scan/", views.scan, name="scan"),
]