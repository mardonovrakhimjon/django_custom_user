from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        admin = "admin", "Admin"
        user = "user", "User"

    is_verified = models.BooleanField(default=False)
    role        = models.TextField(max_length=20, choices=Roles.choices, default=Roles.user)

    def __str__(self):
        return self.username


class UserVerificationCode(models.Model):
    otp = models.BigIntegerField(
        validators=[
            MinValueValidator(100_000),
            MaxValueValidator(999_999)
        ]
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')

    def __str__(self):
        return f"{self.user.email} -> {self.otp}"
