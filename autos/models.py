from django.db import models
from django.core.validators import  MinLengthValidator

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Enter a manufacturer (e.g. Dodge)",
        validators=[MinLengthValidator(2, "Manufacturer must be greater than 1 character")],
    )

    def __str__(self):
        return self.name
    
class Auto(models.Model):
    nickname=models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Nickname must be greater than 1 character")],
    )

    mileage = models.PositiveIntegerField()
    comments = models.CharField(max_length=300)
    make = models.ForeignKey("Manufacturer", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.nickname