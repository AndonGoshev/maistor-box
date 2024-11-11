


from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetCompleteView
from django.urls import path, include

from maistorbox.accounts.views import BaseUserRegistrationView, ContractorUserRegistrationView, CustomLoginView, \
    CustomLogoutView, CustomPasswordChangeView, CustomPasswordChangeDoneView, CustomPasswordResetView, \
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('regular-user/', include([
        path('registration/', BaseUserRegistrationView.as_view(), name='regular-user-registration'),
    ])),
    path('contractors/', include([
        path('registration/', ContractorUserRegistrationView.as_view(), name='contractor-registration')
    ])),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('password-change-done/', CustomPasswordChangeDoneView.as_view(), name='password-change-done'),



    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password-reset-email-sent'),
    path('reset/<str:uidb64>/<str:token>', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]