from django.db import models
from django.core.validators import FileExtensionValidator
from ..pet import Pet
import uuid
# Create your models here.


class Order(models.Model):
    """
    Pet Store Order
    """
    STATUS_CHOICES = (
        (1, "placed"),
        (2, "approved"),
        (3, "delivered")
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    pet = models.ForeignKey(Pet, blank=False, null=False,
                            on_delete=models.PROTECT)

    quantity = models.IntegerField(
        verbose_name='quantity', 
        null=False, 
        blank=False, 
    )
    shipDate = models.DateField(
        blank=True,
        null=True
    )
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    complete = models.BooleanField(
        verbose_name='Active',
        default=False
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
        return self.pet

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = verbose_name
        ordering = ('created_at',)
        db_table = 'tbl_orders'
