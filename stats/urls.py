from django.urls import path

from . import views

app_name = "stats"

urlpatterns = [
    path('urls/', views.WebpageListView.as_view(), name='list'),
]
