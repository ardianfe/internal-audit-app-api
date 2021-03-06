"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def audit_corrective_file_path(instance, filename):
    """Generate file path for new corrective action."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'audit/correctives', filename)




class UserManager(BaseUserManager):
    """Manager for user """

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must input an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Personel(models.Model):
    """Personel object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255, blank=True)
    is_coordinator = models.BooleanField(default=False)
    is_subcoordinator = models.BooleanField(default=False)
    area = models.ForeignKey('Area', blank=True, null=True, on_delete=models.CASCADE)
    sub_area = models.ForeignKey('SubArea', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Area(models.Model):
    """Area for audit filtering."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class SubArea(models.Model):
    """Sub for Area"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Audit(models.Model):
    """NcForm Object."""

    class Category(models.TextChoices):
        MAJOR = 'MJ', _('Major')
        MINOR = 'MI', _('Minor')
        OBSERVASI = 'OBSV', _('Observasi')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    audit_date = models.CharField(max_length=255)
    area = models.ForeignKey('Area', on_delete=models.CASCADE)
    sub_area = models.ForeignKey('SubArea', on_delete=models.CASCADE)
    standard = models.ManyToManyField('Standard', related_name='standards')
    nc_point = models.CharField(max_length=255)
    nc_source = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    verification_note = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    verified_date = models.CharField(max_length=255)
    cat = models.CharField(
        max_length=15,
        choices=Category.choices,
        default=Category.OBSERVASI,
    )

    def __str__(self):
        return self.title


class Correctiveaction(models.Model):
    """Correctiveactions object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )
    cause_analysis = models.TextField(blank=True)
    corrective_actions = models.TextField(blank=True)
    due_date = models.CharField(max_length=255, blank=True)
    prepared_by = models.ForeignKey('Personel', blank=True, on_delete=models.CASCADE)
    pre_actions = models.TextField(blank=True)
    links = models.CharField(max_length=255, blank=True)
    audit = models.OneToOneField('Audit', on_delete=models.CASCADE)
    evidence = models.FileField(null=True, upload_to=audit_corrective_file_path, blank=True)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return self.corrective_actions


class Standard(models.Model):
    """Standard as based for audit"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Standardpoint(models.Model):
    """Standard Point as based for audit."""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    standard_id = models.ForeignKey('Standard', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
