from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Product(models.Model):
    
    code = models.CharField(
        max_length=100,
        verbose_name=_('Code'),
        help_text=_('Code of the product (Max 100)'),
        unique=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
        help_text=_("Name of the product"),
        unique=True
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Detailed description of the product"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
        help_text=_("Indicates if the product is active"),
    )
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} ({status})"
    

class NutritionalInformation(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the nutritional element"),
        unique=True,
    )
    unit = models.CharField(
        max_length=50,
        verbose_name=_("Unit"),
        help_text=_("Unit of measurement (e.g. g, mg, kcal)"),
    )
    class Meta:
        verbose_name = _("Nutritional Information")
        verbose_name_plural = _("Nutritional Information")

    def __str__(self):
        return self.name
    

class ProductNutritionalValue(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='nutritional_values',
        verbose_name=_("Product"),
    )
    nutritional_info = models.ForeignKey(
        'NutritionalInformation',
        on_delete=models.CASCADE,
        verbose_name=_("Nutritional Information"),
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Value"),
        help_text=_("Nutritional value per 100g/ml"),
    )

    class Meta:
        unique_together = ("product", "nutritional_info")
        verbose_name = _("Product Nutritional Value")
        verbose_name_plural = _("Product Nutritional Values")

    def __str__(self):
        return f"{self.product.name} - {self.nutritional_info.name}: {self.value} {self.nutritional_info.unit}"