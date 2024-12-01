import django.contrib.admin
import django.contrib.auth.admin

import users.models


django.contrib.admin.site.register(
    users.models.User,
    django.contrib.auth.admin.UserAdmin,
)
