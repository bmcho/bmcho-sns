from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('/token/refresh', TokenRefreshView.as_view()),
    path('/signup', views.UserSignUpView.as_view()),
    path('/signin', views.UserSignInView.as_view()),
    path('/signout', views.UserSignOutView.as_view()),
    path('/update', views.UserUpdateView.user_update),
]
