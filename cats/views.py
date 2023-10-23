from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from cats.models import Breed, Cat
# Create your views here.

class CatList(LoginRequiredMixin, ListView):
    model = Cat
    template_name = "cats/cat_list.html"
    def get_context_data(self):
        return {"cat_list": Cat.objects.all(), "breed_count": Breed.objects.count()}
    
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = "__all__"
    success_url = reverse_lazy("cats:index")

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = "__all__"
    success_url = reverse_lazy("cats:index")

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = "__all__"
    success_url = reverse_lazy("cats:index")

class BreedList(LoginRequiredMixin, ListView):
    model = Breed
    context_object_name = "breed_list"
    
class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = "__all__"
    success_url = reverse_lazy("cats:index")

class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = "__all__"
    success_url = reverse_lazy("cats:index")

class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    fields = "__all__"
    success_url = reverse_lazy("cats:index")