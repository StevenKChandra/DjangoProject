from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        form.save(commit=False).owner = self.request.user
        form.save()
        return super(OwnerCreateView, self).form_valid(form)
    
class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        return super(OwnerUpdateView, self).get_queryset().filter(owner=self.request.user)
    
class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        return super(OwnerDeleteView, self).get_queryset().filter(owner=self.request.user)