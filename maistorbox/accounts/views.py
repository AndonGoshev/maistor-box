from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from maistorbox.accounts.forms import BaseUserRegistrationForm, ContractorUserRegistrationForm, CustomLoginForm


class BaseUserRegistrationView(CreateView):
    form_class = BaseUserRegistrationForm
    template_name = 'accounts/regular-users/regular-user-registration.html'
    success_url = reverse_lazy('home_page')



class ContractorUserRegistrationView(CreateView):
    form_class = ContractorUserRegistrationForm
    template_name = 'accounts/contractors/contractor-registration.html'
    success_url = reverse_lazy('home_page')

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "accounts/common/login.html"

class CustomLogoutView(LogoutView):
    template_name = "accounts/common/logout.html"
    http_method_names = ['get', 'post', 'options']