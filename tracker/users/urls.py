import django.contrib.auth.views as django_auth
import django.urls

import users.views


app_name = "users"


urlpatterns = [
    django.urls.path(
        "login/",
        django_auth.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    django.urls.path(
        "logout/",
        django_auth.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    django.urls.path(
        "password_change/",
        django_auth.PasswordChangeView.as_view(
            template_name="users/password_change.html",
        ),
        name="password-change",
    ),
    django.urls.path(
        "password_change/done/",
        django_auth.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password-change-done",
    ),
    django.urls.path(
        "password_reset/",
        django_auth.PasswordResetView.as_view(
            template_name="users/password_reset.html",
        ),
        name="password-reset",
    ),
    django.urls.path(
        "password_reset/done/",
        django_auth.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password-reset-done",
    ),
    django.urls.path(
        "reset/<uidb64>/<token>/",
        django_auth.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password-reset-confirm",
    ),
    django.urls.path(
        "reset/done/",
        django_auth.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password-reset-complete",
    ),
    django.urls.path(
        "signup/",
        users.views.SignupViewForm.as_view(),
        name="signup",
    ),
    django.urls.path(
        "activate/<str:username>/<str:token>/",
        users.views.ActiveView.as_view(),
        name="activate",
    ),
]
