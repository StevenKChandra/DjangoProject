from django.forms import ModelForm
from autos.models import Manufacturer

# Create your form class

class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = "__all__"