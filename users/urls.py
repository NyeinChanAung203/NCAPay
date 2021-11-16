from django.urls import path
from . import views


urlpatterns = [
    path('profile/',views.profile,name="profile"),
    path('logout/',views.logoutUser,name="logout"),
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerUser,name="register"),
    path('password/',views.change_password,name="change-password"),
]