from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from .models import Profile
from .forms import ProfileForm, EmailForm
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.views.generic import View
from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['profile'] = self.request.user.profile
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')

        if username:
            # If a username is provided, get that user's profile
            profile = get_object_or_404(User, username=username).profile
        else:
            # If no username is provided, get the logged-in user's profile
            try:
                profile = self.request.user.profile
            except User.profile.RelatedObjectDoesNotExist:
                # Redirect to login if the profile doesn't exist
                return redirect_to_login(self.request.get_full_path())

        # Add the profile to the context
        context['profile'] = profile
        return context

    

# class ProfileView(LoginRequiredMixin, DetailView):
#     model = Profile
#     template_name = 'a_users/profile.html'
#     context_object_name = 'profile'

#     def get_object(self):
#         username = self.kwargs.get('username')

#         if username:
#             # Fetch the profile of the user with the provided username
#             user = get_object_or_404(User, username=username)
#             return user.profile
#         else:
#             # If no username is provided, fetch the current logged-in user's profile
#             try:
#                 return self.request.user.profile
#             except User.profile.RelatedObjectDoesNotExist:
#                 # If the user is not authenticated or has no profile, redirect to login
#                 return redirect_to_login(self.request.get_full_path())


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')  

    def get_object(self):
        return self.request.user.profile 
    

    def form_valid(self, form):
        profile = form.save(commit=False)  
        profile.user = self.request.user  
        profile.save()  
        return redirect('profile')  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path == reverse('profile-onboarding'):
            context['onboarding'] = True
        else:
            context['onboarding'] = False
        return context



class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile_settings.html'




class ProfileEmailChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.htmx:
            form = EmailForm(instance=request.user)
            return render(request, 'partials/email_form.html', {'form': form})
        return redirect('home')
    

    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')

            form.save() 
            # Then Signal updates emailaddress and set verified to False
            # Send confirmation email
            send_email_confirmation(request, request.user)

            messages.success(request, 'Email updated successfully. Please verify your new email.')
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('profile-settings')
 

class ProfileEmailVerifyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        send_email_confirmation(request, request.user)
        return redirect('profile-settings')


class ProfileDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/profile_delete.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request) 
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')