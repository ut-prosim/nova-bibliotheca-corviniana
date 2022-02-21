from django.urls import path
from . import views
from .views import account_redirect

# this like app.use() in express
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.Signup.as_view(), name='signup'),
    path('<int:pk>/profile', views.ProfileView.as_view(), name='profile_view'),
    path('loggedin/', account_redirect, name='loggedin_view'),
    path('<int:pk>/editprofile', views.EditProfileView.as_view(), name='edit_profile_view'),
    path('createprofile/', views.CreateProfileView.as_view(), name='create_profile_view'),
]