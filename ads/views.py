from ads.models import Ad
from django.views.generic import ListView, DetailView
from ads.owner import OwnerCreateView, OwnerUpdateView, OwnerDeleteView

# Create your views here.

class AdListView(ListView):
    model = Ad

class AdDetailView(DetailView):
    model = Ad

class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ["title", "price", "text"]
    
class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ["title", "price", "text"]
    
class AdDeleteView(OwnerDeleteView):
    model = Ad
    # fields = ["title", "price", "text"]