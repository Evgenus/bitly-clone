from django.urls import path

from .views import (
    HomeView,
    RedirectURLView,
)

appname = "shortener"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<str:code>', RedirectURLView.as_view(), name='redirect'),
]