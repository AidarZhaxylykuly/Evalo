from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_question, name='create_question'),
    path('edit/<int:pk>/', views.edit_question, name='edit_question'),
    path('show/<int:pk>/', views.show_question, name='show_question'),
    path('test/create/', views.create_test, name='create_test'),
    path('test/edit/<int:pk>/', views.edit_test, name='edit_test'),
    path('test/show/<int:pk>/', views.show_test, name='show_test'),
]