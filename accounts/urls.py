from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import StyledPasswordChangeForm

app_name = 'accounts'

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            form_class=StyledPasswordChangeForm,
            success_url='/accounts/password-change/done/',
        ),
        name='password_change',
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html',
        ),
        name='password_change_done',
    ),
]
