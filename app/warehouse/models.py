import time
from django.db import models
from django.contrib.auth import get_user_model
from core.utils import get_unique_slug
from core.models import (
    SubDiscipline, MedicineBrand, MedicineCompany,
    Designation
)
from location.models import Location

ACTIVE = 'A'
INACTIVE = 'I'
STATUS = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'In-Active')
)

STOCK_CHOICES = (
        ('I', 'Stock In'),
        ('O', 'Stock Out')
    )


def user_directory_path(instance, filename):
    name = str(int(time.time()))+'.'+filename.split('.')[-1]
    return 'product_{0}/{1}'.format(instance.slug, name)


def agent_directory_path(instance, filename):
    name = str(int(time.time()))+'.'+filename.split('.')[-1]
    return 'agent_{0}/{1}'.format(instance.user.id, name)


class ProductCategory(models.Model):
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


class ProductSubCategory(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    category = models.ForeignKey(
        ProductCategory,
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


class WareHouse(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    discipline = models.ForeignKey(
        SubDiscipline,
        on_delete=models.PROTECT
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


class Product(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    category = models.ForeignKey(
        ProductSubCategory,
        on_delete=models.CASCADE,
        related_name='product_subcategory'
    )
    discipline = models.ForeignKey(
        SubDiscipline,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
    warehouse = models.ForeignKey(
        WareHouse,
        on_delete=models.PROTECT
    )
    remark = models.TextField(blank=True, null=True)    
    is_online_product = models.BooleanField(default=True)
    include_in_prescription = models.BooleanField(default=True)
    required_prescription = models.BooleanField(default=True)
    composition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class ProductTransaction(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    brand = models.ForeignKey(
        MedicineBrand,
        on_delete=models.PROTECT
    )
    company = models.ForeignKey(
        MedicineCompany,
        on_delete=models.PROTECT
    )
    transaction_type = models.CharField(
        max_length=1,
        choices=STOCK_CHOICES
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    rate = models.DecimalField(max_digits=15, decimal_places=4)
    quantity = models.IntegerField()
    discount = models.DecimalField(
        max_digits=15, decimal_places=4,
        blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.product)


class AgentProfile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT
    )
    first_name = models.CharField(
        max_length=255
    )
    middle_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=255
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT
    )
    permanent_address = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='permanent_address'
    )
    profile_pic = models.ImageField(
        upload_to=agent_directory_path,
        blank=True,
        null=True
    )
    warehouse = models.ManyToManyField(
        WareHouse
    )

    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.phone_number
