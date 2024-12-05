import django.contrib.admin
import django.contrib.auth
import django.contrib.auth.admin


user_model = django.contrib.auth.get_user_model()


django.contrib.admin.site.register(
    user_model,
    django.contrib.auth.admin.UserAdmin,
)
