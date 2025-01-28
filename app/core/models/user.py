import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import NotAcceptable
from .base import BaseModel


User = get_user_model()


class PhoneNumber(BaseModel):
    user = models.OneToOneField(User, related_name="phone", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, db_index=True)
    security_code = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)

    class Meta:
        db_table = "users_phonenumber"
        ordering = ("-created_at",)

    def __str__(self):
        return self.phone_number.as_e164

    def generate_security_code(self):
        """
        Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
        Default token length = 6
        """
        token_length = getattr(settings, "TOKEN_LENGTH", 6)
        return get_random_string(token_length, allowed_chars="0123456789")

    def is_security_code_expired(self):
        expiration_date = self.sent + datetime.timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        return expiration_date <= timezone.now()

    def send_confirmation(self):
        self.security_code = self.generate_security_code()
        
        print(f"Your activation code for phone number {self.phone_number} is {self.security_code}")

        self.sent = timezone.now()
        self.save()
        return True

        # twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        # twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        # twilio_phone_number = settings.TWILIO_PHONE_NUMBER

        # if all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
        #     try:
        #         twilio_client = Client(twilio_account_sid, twilio_auth_token)
        #         twilio_client.messages.create(
        #             body=f"Your activation code is {self.security_code}",
        #             to=str(self.phone_number),
        #             from_=twilio_phone_number,
        #         )
        #         self.sent = timezone.now()
        #         self.save()
        #         return True
        #     except TwilioRestException as e:
        #         print(e)
        # else:
        #     print("Twilio credentials are not set")

    def check_verification(self, security_code):
        if (
            not self.is_security_code_expired()
            and security_code == self.security_code
            and self.is_verified == False
        ):
            self.is_verified = True
            self.save()
        else:
            raise NotAcceptable(
                _("Your security code is wrong, expired or this phone is verified before.")
            )

        return self.is_verified


class Profile(BaseModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar", blank=True)
    bio = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "users_profile"
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()


class Address(BaseModel):
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_address"
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()
