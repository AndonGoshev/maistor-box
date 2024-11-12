from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetCompleteView
from django.urls import path, include

from django.conf import settings
from maistorbox.accounts.views import BaseUserRegistrationView, ContractorUserRegistrationView, CustomLoginView, \
    CustomLogoutView, CustomPasswordChangeView, CustomPasswordChangeDoneView, CustomPasswordResetView, \
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, RegularUserProfileView, UserProfileDeleteView, \
    ContractorUserProfileDetailsView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('regular-user/', include([
        path('registration/', BaseUserRegistrationView.as_view(), name='regular-user-registration'),
        path('profile-details/<int:id>/', RegularUserProfileView.as_view(), name='regular-user-profile-details'),
    ])),
    path('contractors/', include([
        path('registration/', ContractorUserRegistrationView.as_view(), name='contractor-registration'),
        path('profile-details/<int:id>/', ContractorUserProfileDetailsView.as_view(), name='contractor-user-profile-details')
    ])),

    path('profile-delete/<int:id>/', UserProfileDeleteView.as_view(), name='user-profile-delete'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('password-change-done/', CustomPasswordChangeDoneView.as_view(), name='password-change-done'),



    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password-reset-email-sent'),
    path('reset/<str:uidb64>/<str:token>', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
