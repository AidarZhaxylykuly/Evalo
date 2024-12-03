from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import ProfileForm, FolderForm
from .models import Profile, Follow, TestsFolder
from tests.models import Test
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, UserSerializer
from .permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegisterAPIView(APIView):
    """Регистрация нового пользователя через API"""

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создаёт нового пользователя в системе",
        request_body=UserSerializer,
        responses={
            201: openapi.Response("Пользователь успешно зарегистрирован"),
            400: "Ошибка валидации данных"
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Выход из системы"""

    @swagger_auto_schema(
        operation_summary="Выход пользователя",
        operation_description="Выходит из системы",
        responses={200: "Успешный выход"}
    )
    def post(self, request):
        return Response({"message": "Successfully logged out"}, status=200)


class ProtectedView(APIView):
    """Защищённый ресурс"""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Доступ к защищённому ресурсу",
        operation_description="Доступ возможен только для аутентифицированных пользователей",
        responses={200: "Доступ разрешён"}
    )
    def get(self, request):
        return Response({"message": "This is a protected view."})


class AdminOnlyView(APIView):
    """Ресурс только для администраторов"""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_summary="Доступ для администраторов",
        operation_description="Доступ возможен только для пользователей с правами администратора",
        responses={200: "Доступ разрешён"}
    )
    def get(self, request):
        return Response({"message": "This is an admin-only view."})


class ProfileViewSet(viewsets.ModelViewSet):
    """CRUD операции для профилей"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить список профилей",
        operation_description="Возвращает список всех профилей в системе",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать профиль",
        operation_description="Создаёт новый профиль для пользователя",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить профиль",
        operation_description="Возвращает профиль по ID",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить профиль",
        operation_description="Обновляет данные профиля по ID",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить профиль",
        operation_description="Удаляет профиль по ID",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UserRegister(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        return super().form_valid(form)


class EditProfileView(generic.UpdateView):
    form_class = ProfileForm
    template_name = 'profile/profile_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.profile


def profile(request, pk):
    user = get_object_or_404(User, id=pk)
    profile = get_object_or_404(Profile, user=user)
    is_follower = Follow.objects.filter(follower=request.user, following=user).exists()
    users = User.objects.exclude(id=request.user.id)
    context = {
        'profile': profile,
        'is_follower': is_follower,
        'users': users,
    }
    return render(request, "profile/profile.html", context)


def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('home')


def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('home')


def create_folder(request):
    """Создание новой папки"""
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            form.save_m2m()
            return redirect('my-folders')
    else:
        form = FolderForm()
    return render(request, 'folders/folder_form.html', {'form': form})


def user_tests(request):
    """Отображение тестов, созданных и пройденных пользователем"""
    created_tests = Test.objects.filter(author=request.user)
    passed_tests = Test.objects.filter(allowed_users=request.user)

    context = {
        'created_tests': created_tests,
        'passed_tests': passed_tests,
    }
    return render(request, 'tests/user_tests.html', context)


def my_folders(request):
    """Отображение папок пользователя"""
    folders = TestsFolder.objects.filter(owner=request.user)
    return render(request, 'folders/folder_list.html', {'folders': folders})
