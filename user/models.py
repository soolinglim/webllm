from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):   
    def _create_user(self, email, password, is_staff, is_superuser):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),
            is_staff=is_staff, is_active=True, is_superuser=is_superuser,
            date_joined=now)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password):
        return self._create_user(email, password, False, False)
    
    def create_superuser(self, email, password):
        return self._create_user(email, password, True, True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), max_length=255, blank=False, unique=True, db_index=True)
    is_staff = models.BooleanField(('staff'), default=False, 
        help_text=('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(('active'), default=True,
        help_text=('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
