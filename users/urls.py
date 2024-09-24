from django.urls import path
from .views import ProfileView, ProfileEditView, ProfileSettingsView, ProfileEmailChangeView, ProfileEmailVerifyView, ProfileDeleteView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('onboarding/',ProfileEditView.as_view(), name="profile-onboarding"),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('profile/emailchange/', ProfileEmailChangeView.as_view(), name='profile-emailchange'),
    path('profile/emailverify/', ProfileEmailVerifyView.as_view(), name='profile-emailverify'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile-delete'),

    
]
