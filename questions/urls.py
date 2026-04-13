from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('quiz/<str:category>/', views.quiz_page, name='quiz_page'),  
    path('quiz_complete/', views.quiz_complete, name='quiz_complete'), 
]
