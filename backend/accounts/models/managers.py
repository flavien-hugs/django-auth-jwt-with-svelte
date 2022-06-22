# accounts.models.managers.py

from typing import Optional

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    """
    UserManager class
    """

    def _create_user(
        self, phone: str,
        password: Optional[str] = None,
        **extra_fields
    ) -> 'User':

        if not phone:
            raise TypeError("Le numéro de téléphone donné doit être défini !")

        now = timezone.now()
        self.phone = phone
        user = self.model(
            phone=phone, is_active=True,
            last_login=now, date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone: str, password: str, **extra_fields) -> 'User':

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone: str, password: str, **extra_fields) -> 'User':

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le super-utilisateur doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                "Le super-utilisateur doit avoir is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)
