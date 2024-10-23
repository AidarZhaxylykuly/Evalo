from django.urls import path 
from .views import UserRegister, EditProfileView , profile , follow_user , unfollow_user


urlpatterns = [
    path('register/', UserRegister.as_view(), name = 'register'),
    path('profile/<int:pk>/', profile , name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name = 'profile-edit'),
    path('profile/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('profile/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    path('profile/1/', profile, name='home'),
]