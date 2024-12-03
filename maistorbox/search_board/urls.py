from django.urls import path

from maistorbox.search_board.views import SearchBoardView

urlpatterns = [
    path('contractors-search', (SearchBoardView.as_view), name='search_board'),
]