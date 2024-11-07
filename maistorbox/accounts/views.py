from http.client import responses

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from maistorbox.accounts.forms import ContractorUserRegistrationForm, RegularUserRegistrationForm
from maistorbox.accounts.models import ContractorUser


class ContractorUserRegistrationView(CreateView):
    model = ContractorUser
    form_class = ContractorUserRegistrationForm
    template_name = 'accounts/contractors/contractor-registration.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class RegularUserRegistrationView(CreateView):
    form_class = RegularUserRegistrationForm
    template_name = 'accounts/regular-users/regular-user-registration.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = "accounts/common/login.html"

class CustomLogoutView(LogoutView):
    template_name = "accounts/common/logout.html"
    http_method_names = ['get', 'post', 'options']