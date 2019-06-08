from django.db import models
# Create your models here.


class City(models.Model):
    """ City model """
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
    zip_code = models.CharField(
        verbose_name='zip_code',
        null=False,
        blank=False,
        max_length=50
    )
    created_at = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )

    def __str__(self):
        return "{} - {}".format(self.name, str(self.zip_code))
    #     return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = verbose_name
        ordering = ['name',]
        db_table = 'tbl_cities'
