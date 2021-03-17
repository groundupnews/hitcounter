from django.urls import path

from . import views

app_name = "stats"

urlpatterns = [
    path('urls/', views.url_view, name='list'),
]
