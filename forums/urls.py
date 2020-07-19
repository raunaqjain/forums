"""forums URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from accounts import views as accounts_views
from boards import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'signup/', accounts_views.signup, name='signup'),
    path(r'login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(r'reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    path(r'reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path(r'reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    path(r'settings/password/', 
        auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path(r'settings/password/done/', 
        auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    path(r'boards/<int:pk>/topic/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path(r'boards/<int:pk>/topic/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path(r'boards/<int:pk>/topic/<int:topic_pk>/posts/<int:edit_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path(r'boards/<int:pk>/', views.board_topics, name='board_topics'),
    path(r'boards/<int:pk>/new/', views.new_topic, name='new_topic'),
    path(r'admin/', admin.site.urls),
]