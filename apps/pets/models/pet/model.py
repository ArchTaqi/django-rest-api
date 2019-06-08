from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from ..city import City
import uuid
# Create your models here.

User = settings.AUTH_USER_MODEL


class PetCategory(models.Model):
    """ PetCategory model """
    id = models.AutoField(
        primary_key=True
    )

    name = models.CharField(
        verbose_name='Name',
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        db_index=True
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True,
        default='',
        max_length=5000
    )
    active = models.BooleanField(
        verbose_name='Active',
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pet Category"
        verbose_name_plural = verbose_name
        ordering = ('created_at',)
        db_table = 'tbl_pet_categories'


class Tag(models.Model):
    """ Tag model """
    id = models.AutoField(
        primary_key=True
    )

    name = models.CharField(
        verbose_name='Name',
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        db_index=True
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True,
        default='',
        max_length=5000
    )
    active = models.BooleanField(
        verbose_name='Active',
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = verbose_name
        ordering = ('created_at',)
        db_table = 'tbl_tags'


class Pet(models.Model):
    """
    class: Class Pet contains all the fields needed to create an object
    """
    STATUS_CHOICES = (
        (1, "available"),
        (2, "pending"),
        (3, "sold")
    )
    owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='pets',
        on_delete=models.SET_NULL
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # doggie
    name = models.CharField(
        verbose_name='Name',
        max_length=128,
        null=False,
        blank=False,
        #unique=True,
    ) 
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True,
        default='',
        max_length=5000
    )
    category = models.ForeignKey(
        PetCategory,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True,
        null=True,
    )
    city = models.ForeignKey(
        City,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    photoUrls = models.FileField(
        upload_to='pets/',
        blank=False,
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])]
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )

    latitude = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    longitude = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    contact_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    mailing_address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    facebook = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )
    twitter = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Last Modified",
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = verbose_name
        ordering = ('created_at',)
        db_table = 'tbl_pets'
