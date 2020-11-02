from django.contrib.auth.backends import ModelBackend
from users.models import User


class SNSAuthBackend(ModelBackend):
    def authenticate(
        self, username=None, google_id=None, facebook_id=None, apple_id=None
    ):
        try:
            if google_id:
                return User.objects.get(username=username, google_id=google_id)
            elif facebook_id:
                return User.objects.get(username=username, facebook_id=facebook_id)
            elif apple_id:
                return User.objects.get(username=username, apple_id=apple_id)
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
