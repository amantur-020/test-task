from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.urls import path
from . import views


urlpatterns = [
    path('', views.BaseView.as_view(), name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('tests/', views.TestListView.as_view(), name='tests'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='questions'),
    path('test_result/<int:pk>/', views.TestResultDetailView.as_view(), name='test_result')
]