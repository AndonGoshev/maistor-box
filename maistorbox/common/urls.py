from django.urls import path

from maistorbox.common.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page')
]