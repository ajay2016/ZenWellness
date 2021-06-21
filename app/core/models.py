import time
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Permission
)
from django.core.validators import (
    MinLengthValidator
)
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from .constants import (
    ONLINE_USER, STAFF, AGENT, DOCTOR, PATIENT,
    ACTIVE, INACTIVE, LAB
)
from location.models import Location
from .utils import get_unique_slug


STATUS = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'In-Active')
)


def user_directory_path(instance, filename):
    name = str(int(time.time()))+'.'+filename.split('.')[-1]
    return 'agent_{0}/{1}'.format(instance.user.id, name)


class UserAccountModelManager(BaseUserManager):
    def create_user(self, phone_number, password, user_type=None):
        """
        Creates and saves a User with the given phone number, password
        and user type.
        """
        if not phone_number or not password:
            raise ValueError('Users must have phone number and password')

        user = self.model(
            phone_number=phone_number,
        )
        if user_type is None:
            user_type = ONLINE_USER
        user.user_type = user_type
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        """
        Creates and saves a superuser with the given phone number and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            user_type=STAFF
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    USER_TYPE = (
        (ONLINE_USER, 'Online User'),
        (STAFF, 'Staff'),
        (AGENT, 'Agent'),
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
        (LAB, 'Lab')
    )
    phone_number = models.CharField(
        name=_('phone_number'),
        max_length=10,
        validators=[MinLengthValidator(10)],
        unique=True
    )
    user_type = models.CharField(
        name=_('user_type'),
        max_length=1,
        choices=USER_TYPE,
        default=ONLINE_USER
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    permissions = models.ManyToManyField(
        Permission
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_type']

    objects = UserAccountModelManager()

    def __str__(self):
        return str(self.phone_number)

    @property
    def is_staff(self):
        return self.is_admin


class Discipline(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class SubDiscipline(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE
    )
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class Designation(models.Model):
    title = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)


class University(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    location = models.CharField(
        max_length=255
    )
    website_link = models.CharField(
        max_length=255
    )
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class Degree(models.Model):
    title = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    university = models.ManyToManyField(University)
    detail = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)


class MedicineBrand(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class MedicineCompany(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)