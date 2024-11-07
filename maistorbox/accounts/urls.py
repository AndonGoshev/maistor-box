from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from maistorbox.accounts.views import RegularUserRegistrationView, ContractorUserRegistrationView, CustomLoginView, \
    CustomLogoutView



urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('regular-user/', include([
        path('registration/', RegularUserRegistrationView.as_view(), name='regular-user-registration'),
    ])),
    path('contractors/', include([
        path('registration/', ContractorUserRegistrationView.as_view(), name='contractor-registration')
    ]))
]