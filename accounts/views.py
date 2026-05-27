from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import RegisterForm, LoginForm, ProfileForm
from cars.models import Car, Favorite


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
                city=form.cleaned_data.get('city', 'Бишкек'),
            )
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


@login_required
def profile(request):
    prof, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=prof, initial={'first_name': request.user.first_name, 'last_name': request.user.last_name})
    return render(request, 'accounts/profile.html', {'form': form, 'profile': prof})


@login_required
def my_ads(request):
    cars = Car.objects.filter(seller=request.user).prefetch_related('images').order_by('-created_at')
    return render(request, 'accounts/my_ads.html', {'cars': cars})


@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('car__brand', 'car__model').prefetch_related('car__images')
    return render(request, 'accounts/my_favorites.html', {'favorites': favorites})


def seller_profile(request, pk):
    seller = get_object_or_404(User, pk=pk)
    cars = Car.objects.filter(seller=seller, is_active=True).prefetch_related('images')
    prof, _ = UserProfile.objects.get_or_create(user=seller)
    return render(request, 'accounts/seller_profile.html', {'seller': seller, 'cars': cars, 'profile': prof})