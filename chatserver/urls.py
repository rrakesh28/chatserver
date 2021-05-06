"""chatserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from personal.views import (
    home_view,
)
from account.views import (
    account_view,
    account_search_view,
    logout_view,
    login_view,
    register_view,
    search_page_view,
)

from post.views import(
    post_page_view,
    add_post,
)

urlpatterns = [
    path('',home_view,name='home'),
    path('admin/', admin.site.urls),
    path('account/',include('account.urls',namespace='account')),
    path('friend/',include('friend.urls',namespace='friend')),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('post/',post_page_view,name='post_page'),
    path('add_post/',add_post,name='add_post'),
    path('register/',register_view,name='register'),
    path('search/',account_search_view,name='search'),
    path('search_page',search_page_view,name='search_page'),

     # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
