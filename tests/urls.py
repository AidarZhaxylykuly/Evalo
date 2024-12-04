from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home,create_test, show_test, edit_test, delete_test, add_user_to_test, delete_user_from_test, pass_test, \
    submit_test, test_result, QuestionViewSet, CategoryViewSet, TestViewSet, AnswerBlankViewSet, manage_allowed_users

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'answerblanks', AnswerBlankViewSet, basename='answerblank')

urlpatterns = [
    path('', home, name='home'),
    path('', include(router.urls)),
    path('test/create/', create_test, name='create_test'),
    path('test/<int:test_id>/', show_test, name='show_test'),
    path('test/<int:test_id>/manage_allowed_users/', manage_allowed_users, name='manage_allowed_users'),
    path('test/<int:test_id>/edit/', edit_test, name='edit_test'),
    path('test/<int:test_id>/delete/', delete_test, name='delete_test'),
    path('test/<int:test_id>/add_user/', add_user_to_test, name='add_user_to_test'),
    path('test/<int:test_id>/delete_user/', delete_user_from_test, name='delete_user_from_test'),

    path('test/<int:test_id>/pass/', pass_test, name='pass_test'),
    path('test/<int:test_id>/submit/', submit_test, name='submit_test'),
    path('test/<int:test_id>/result/', test_result, name='test_result'),
]
