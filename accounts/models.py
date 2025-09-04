from django.utils import timezone
from datetime import timedelta

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

#accounts/models.py
class User(AbstractUser):
    GENDER = (('male', 'Male'), ('female', 'Female'))
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = PhoneNumberField(null=True, unique=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return self.username

    @property
    def is_online(self):
        if self.last_seen:
            return timezone.now() - self.last_seen < timedelta(minutes=5)
        return False

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower","following")