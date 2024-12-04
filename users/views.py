from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render , redirect , get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm , UserChangeForm 
from django.urls import reverse_lazy
from .forms import ProfileForm, FolderForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow, TestsFolder
from tests.models import Test
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, UserSerializer
from .permissions import IsAdmin


class UserRegisterAPIView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Successfully logged out"}, status=200)
    
    
class ProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view."})
    
class AdminOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "This is an admin-only view."})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
    user = get_object_or_404(User, id = pk)
    profile = get_object_or_404(Profile, user=user)
    is_follower = Follow.objects.filter(follower=request.user, following=user).exists()
    users = User.objects.exclude(id=request.user.id)
    context = {
        'profile': profile,
        'is_follower': is_follower, 
        'users': users, 
    }
    return render(request, "profile/profile.html" , context)

@login_required 
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('home')
    
@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = User.objects.get(id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('home')


@login_required
def create_folder(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized access"}, status=401)
    
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
    created_tests = Test.objects.filter(author=request.user)
    passed_tests = Test.objects.filter(allowed_users=request.user)

    context = {
        'created_tests': created_tests,
        'passed_tests': passed_tests,
    }
    return render(request, 'tests/user_tests.html', context)

@login_required
def my_folders(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized access"}, status=401)
    folders = TestsFolder.objects.filter(owner=request.user)
    return render(request, 'folders/folder_list.html', {'folders': folders})

def folder_detail(request, folder_id):
    folder = get_object_or_404(TestsFolder, id=folder_id, owner=request.user)
    tests = folder.test_blanks.all()
    context = {
        'folder': folder,
        'tests': tests,
    }
    return render(request, 'folders/folder_detail.html', context)

@login_required
def edit_folder(request, folder_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized access"}, status=401)
    
    folder = get_object_or_404(TestsFolder, id=folder_id, owner=request.user)

    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('folder-detail', folder_id=folder.id)
    else:
        form = FolderForm(instance=folder)

    return render(request, 'folders/folder_form.html', {'form': form, 'folder': folder})

@login_required
def delete_folder(request, folder_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized access"}, status=401)
    
    folder = get_object_or_404(TestsFolder, id=folder_id)

    if folder.owner != request.user:
        return HttpResponseForbidden("You do not have permission to delete this folder.")

    if request.method == 'POST':
        folder.delete()
        return redirect('my-folders')
    
    return render(request, 'folders/folder_confirm_delete.html', {'folder': folder})