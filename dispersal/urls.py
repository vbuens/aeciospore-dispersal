from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run/', views.run, name='run'),
    path('run/results/', views.results,name='results'),
    path('about/', views.about,name='about'),
#    path('run/results/q=<int:source>/', views.results, name='results'),
]
