from django.views import generic
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse

from ads.owner import OwnerDeleteView
from ads.models import Ad, Comment
from ads.forms import CommentForm, CreateForm
# Create your views here.

class AdListView(generic.ListView):
    model = Ad

class AdDetailView(generic.DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        context = {}
        context["ad"] = get_object_or_404(Ad, id=pk)
        context["comments"] = Comment.objects.filter(ad=ad).order_by("-updated_at")
        context["comment_form"] = CommentForm()

        return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    template_name = "ads/ad_form.html"
    success_url = "ads:index"
    
    def get(self, request):
        context = {"form": CreateForm()}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            context = {"form": form}
            return render(request, self.template_name, context)

        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()

        return redirect(self.success_url)

    
class AdUpdateView(LoginRequiredMixin, View):
    template_name = "ads/ad_form.html"
    success_url = "ads:index"
    
    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=request.user)
        context = {"form": CreateForm(instance=ad)}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            context = {"form": form}
            return render(request, self.template_name, context)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)
    
class AdDeleteView(OwnerDeleteView):
    model = Ad

class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        
        return redirect(reverse("ads:detail", args=[pk]))
    
class CommentDeleteView(OwnerDeleteView):
    model = Comment

    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:detail', args=[ad.id])
    
def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response