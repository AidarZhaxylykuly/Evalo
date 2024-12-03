from django.urls import path, include 
from .views import  ProtectedView, AdminOnlyView, UserRegisterAPIView, ProfileViewSet, UserRegister, LogoutView, EditProfileView , profile , follow_user , unfollow_user, user_tests, create_folder, my_folders
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegisterAPIView.as_view(), name='api-register'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/protected/', ProtectedView.as_view(), name='protected-view'),
    path('api/admin-only/', AdminOnlyView.as_view(), name='admin-only-view'),
    
    path('register/', UserRegister.as_view(), name = 'register'),
    path('profile/<int:pk>/', profile , name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name = 'profile-edit'),
    path('profile/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('profile/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    path('my-tests/', user_tests, name='user-tests'),
    path('folders/create/', create_folder, name='create-folder'),
    path('folders/', my_folders, name='my-folders'),
]