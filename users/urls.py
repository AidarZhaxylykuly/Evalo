from django.urls import path 
from .views import UserRegister, EditProfileView , profile , follow_user , unfollow_user, user_tests, create_folder, my_folders


urlpatterns = [
    path('register/', UserRegister.as_view(), name = 'register'),
    path('profile/<int:pk>/', profile , name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name = 'profile-edit'),
    path('profile/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('profile/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    path('my-tests/', user_tests, name='user-tests'),
    path('folders/create/', create_folder, name='create-folder'),
    path('folders/', my_folders, name='my-folders'),
]