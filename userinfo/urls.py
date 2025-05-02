from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserInfoView.as_view(), name='user-profile'),
]
