from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my-ads/', views.my_ads, name='my_ads'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('seller/<int:pk>/', views.seller_profile, name='seller_profile'),
]