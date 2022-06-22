# accounts.models.users.py

import uuid
from typing import Any, Optional

from django.db import models

from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = PhoneNumberField(
        unique=True, null=True,
        error_messages={
            'unique': "Ce numéro téléphone est déjà utilisé \
            par un autre utilisateur."
        },
        verbose_name='Téléphone mobile',
    )
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(null=True)
    full_name = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(null=True)

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['id'])]
        verbose_name_plural = "users"

    def __str__(self) -> str:
        string = self.email if self.email != '' else self.get_full_name()
        return f'{self.id} {string}'

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def get_full_name(self) -> Optional[str]:
        return self.full_name

    def get_short_name(self) -> str:
        return self.username
