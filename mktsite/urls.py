"""mktsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from sell import views as sell_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
       path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('', include('sell.urls')),

    path('category/electronic',sell_views.ItemFilter_electronic.as_view(),name='item_filter_electronic'),
    path('category/car',sell_views.ItemFilter_car.as_view(),name='item_filter_car'),
    path('category/books',sell_views.ItemFilter_books.as_view(),name='item_filter_books'),
    path('category/furniture',sell_views.ItemFilter_furniture.as_view(),name='item_filter_furniture'),
    path('category/sports',sell_views.ItemFilter_sports.as_view(),name='item_filter_sports'),
    path('category/clothes',sell_views.ItemFilter_clothes.as_view(),name='item_filter_clothes'),
    path('category/free',sell_views.ItemFilter_free.as_view(),name='item_filter_free'),
    path('category/others',sell_views.ItemFilter_others.as_view(),name='item_filter_others'),

    path('search/title/',sell_views.SearchTitleListView.as_view(),name='search_title'),
    path('nearby/',sell_views.PostListView.as_view(), name='item_filter_nearby'),
    path('country/',sell_views.PostListViewCountry.as_view(), name='item_filter_country'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
