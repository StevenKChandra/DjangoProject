from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from autos.models import Manufacturer, Auto
from autos.forms import ManufacturerForm
# Create your views here.

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        mc = Manufacturer.objects.count()
        al = Auto.objects.all()

        context = {"manufacturer_count": mc, "auto_list": al}
        return render(request, "autos/auto_list.html", context)
    
class ManufacturerView(LoginRequiredMixin, View):
    def get(self, request):
        ml = Manufacturer.objects.all()

        context = {"manufacturer_list": ml}
        return render(request, "autos/manufacturer_list.html", context)

class ManufacturerCreate(LoginRequiredMixin, View):
    template = "autos/manufacturer_form.html"
    success_url = reverse_lazy("autos:index") # render_lazy because the class is constructed before loading urls.py

    def get(self, request):
        form = ManufacturerForm()
        
        context = {"form": form}
        return render(request, self.template, context)
    
    def post(self, request):
        form = ManufacturerForm(request.POST)
        if not form.is_valid():
            context = {"form": form}
            return render(request, self.template, context)

        form.save()
        return redirect(self.success_url)

class ManufacturerUpdate(LoginRequiredMixin, View):
    model = Manufacturer
    template = "autos/manufacturer_form.html"
    success_url = reverse_lazy("autos:index")

    def get(self, request, pk):
        manufacturer = get_object_or_404(self.model, pk=pk)
        form = ManufacturerForm(instance=manufacturer)
        
        context = {"form": form}
        return render(request, self.template, context)
    
    def post(self, request, pk):
        manufacturer = get_object_or_404(self.model, pk=pk)
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if not form.is_valid():
            context = {"form": form}
            return render(request, self.template, context)

        form.save()
        return redirect(self.success_url)
    
class ManufacturerDelete(LoginRequiredMixin, View):
    model = Manufacturer
    template = "autos/manufacturer_confirm_delete.html"
    success_url = reverse_lazy("autos:index")

    def get(self, request, pk):
        manufacturer = get_object_or_404(self.model, pk=pk)

        context = {"manufacturer": manufacturer}
        return render(request, self.template, context)
    
    def post(self, request, pk):
        manufacturer = get_object_or_404(self.model, pk=pk)
        manufacturer.delete()
        return redirect(self.success_url)
    
class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    fields = "__all__"
    success_url = reverse_lazy('autos:index')

class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = "__all__"
    success_url = reverse_lazy('autos:index')
    
class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = "__all__"
    success_url = reverse_lazy('autos:index')