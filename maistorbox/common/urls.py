from django.urls import path

from maistorbox.common.views import HomePageView, ContractorPublicProfileView, LoginRequiredView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('login-required/', LoginRequiredView.as_view(), name='login-required'),
    path('<slug:slug>/', ContractorPublicProfileView.as_view(), name='contractor-public-profile'),
]