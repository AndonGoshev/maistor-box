from django.urls import path

from maistorbox.common.views import HomePageView, ContractorPublicProfileView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('<slug:slug>/', ContractorPublicProfileView.as_view(), name='contractor-public-profile'),
]