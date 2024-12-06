from django.urls import path

from maistorbox.common.views import HomePageView, ContractorPublicProfileView, LoginRequiredView, AboutUsView, \
    ContactsView, SentSuccessfullyView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('sent-successfully/', SentSuccessfullyView.as_view(), name='sent_successfully'),
    path('login-required/', LoginRequiredView.as_view(), name='login-required'),
    path('<slug:slug>/', ContractorPublicProfileView.as_view(), name='contractor-public-profile'),
]