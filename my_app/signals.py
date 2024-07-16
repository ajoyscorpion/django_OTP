from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from .models import Users

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    social_account = user.socialaccount_set.first()
    if social_account:
        extra_data = social_account.extra_data
        user.name = extra_data.get('name', '')
        # Assuming phone number might not be available through allauth's default data
        user.phone_number = extra_data.get('phone_number', '') if 'phone_number' in extra_data else ''
        user.save()
# def social_account_signup(request,user, **kwargs):
#     social_account = SocialAccount.objects.get(user=user)
#     print(social_account)
#     extra_data = social_account.extra_data
#     print(extra_data)

#     name = extra_data.get('name')
#     print(name)
#     email = extra_data.get('email')
#     print(email)
#     phone = extra_data.get('phone_number')
#     print(phone)

#     user_profile = Users.objects.get_or_create(user=user)
#     user_profile.name = name
#     user_profile.email = email
#     user_profile.phone_number = phone
#     print(user_profile)
#     user_profile.save()