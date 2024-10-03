from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UsernameEmailPhoneBackend(ModelBackend):
  def authenticate(self, request, username: str="", password: str="", **kwargs):
        UserModel = get_user_model()
        try:
            # Check if the identifier is an email, phone number, or username
            if '@' in username:
                user = UserModel.objects.get(email=username)
            elif username.isdigit():
                user = UserModel.objects.get(phone_number=username)
            else:
                user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user