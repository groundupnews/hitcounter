from django.urls import path

from counter import views

app_name = 'counter'

urlpatterns = [
    path('hit/<slug:site>/<slug:slug>/', views.hit_view, name='hit'),
]
