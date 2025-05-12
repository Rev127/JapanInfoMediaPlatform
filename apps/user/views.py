from django.shortcuts import render, redirect
from pyexpat.errors import messages

from .facade import UserViewer
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib import messages

# Create your views here.

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def profile_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'avatar_update':
            update_value = request.FILES.get('update_value')
        else:
            update_value = request.POST.get('update_value')

        if UserViewer.update_profile(action, update_value, request.user):
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "Profile update failed.")

        return redirect('profile')

    user_id = request.user.id
    user = UserViewer.get_user_by_id(user_id)
    return render(request, 'user/profile.html', {
        'user': user
    })
