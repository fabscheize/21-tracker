import django.contrib.auth
import django.utils.deprecation


user_model = django.contrib.auth.get_user_model()

__all__ = ()


class CustomUserMiddleware(django.utils.deprecation.MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user = user_model.objects.get(pk=request.user.pk)
