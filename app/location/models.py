from django.db import models


ACTIVE = 'A'
INACTIVE = 'I'
STATUS = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive')
)


class Country(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )

    def __str__(self):
        return self.name
