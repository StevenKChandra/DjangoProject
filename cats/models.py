from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Breed(models.Model):
    breed_name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Breed must be greater than 1 character")]
    )

    def __str__(self):
        return self.breed_name

class Cat(models.Model):
    cat_name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Name must be greater than 1 character")]
    )
    weight = models.PositiveIntegerField()
    foods = models.CharField(max_length=300)
    breed = models.ForeignKey("breed", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.cat_name
