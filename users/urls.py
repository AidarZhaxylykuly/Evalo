<<<<<<< Updated upstream
from django.urls import path 
from .views import UserRegister, EditProfileView , profile , follow_user , unfollow_user, home, user_tests, create_folder, my_folders

=======
from django.urls import path, include 
from .views import  ProtectedView, AdminOnlyView, UserRegisterAPIView, ProfileViewSet, UserRegister, LogoutView, EditProfileView, delete_folder, edit_folder , profile , follow_user , unfollow_user, user_tests, create_folder, my_folders, folder_detail
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
>>>>>>> Stashed changes


urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegister.as_view(), name = 'register'),
    path('profile/<int:pk>', profile , name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name = 'profile-edit'),
    path('profile/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('profile/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    path('my-tests/', user_tests, name='user-tests'),

    path('folders/create/', create_folder, name='create-folder'),
    path('folders/', my_folders, name='my-folders'),
    path('folders/<int:folder_id>/', folder_detail, name='folder-detail'),
    path('folders/<int:folder_id>/edit/', edit_folder, name='edit-folder'),
    path('folders/<int:folder_id>/delete/', delete_folder, name='delete-folder'),

]