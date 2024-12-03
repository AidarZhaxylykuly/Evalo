from django.urls import path
from .views import home,create_test, show_test, edit_test, delete_test, add_user_to_test, delete_user_from_test, pass_test, \
    submit_test, test_result

urlpatterns = [
    path('', home, name='home'),
    path('test/create/', create_test, name='create_test'),
    path('test/<int:test_id>/', show_test, name='test_detail'),
    path('test/<int:test_id>/edit/', edit_test, name='edit_test'),
    path('test/<int:test_id>/delete/', delete_test, name='delete_test'),
    path('test/<int:test_id>/add_user/', add_user_to_test, name='add_user_to_test'),
    path('test/<int:test_id>/delete_user/', delete_user_from_test, name='delete_user_from_test'),

    path('<int:test_id>/pass/', pass_test, name='pass_test'),
    path('<int:test_id>/submit/', submit_test, name='submit_test'),
    path('test/<int:test_id>/result/', test_result, name='test_result'),
]
