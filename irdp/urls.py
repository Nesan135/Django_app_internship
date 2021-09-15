from django.urls import path

from .views import HomePageView, SearchResultsView,external,external_test

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', HomePageView.as_view(), name='home'),
    path('external/', external, name='external_results'),
    path('externaltest/', external_test, name='external_results_test'),
]