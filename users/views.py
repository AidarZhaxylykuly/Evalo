from django.shortcuts import render , redirect , get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm , UserChangeForm 
from django.urls import reverse_lazy
from .forms import ProfileForm
from django.contrib.auth.models import User
from .models import Profile, Follow, TestsFolder


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
    
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('home')
    
def unfollow_user(request, user_id):
    user_to_unfollow = User.objects.get(id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('home')
