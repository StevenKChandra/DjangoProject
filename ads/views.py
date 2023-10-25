from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from ads.owner import OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from ads.models import Ad, Comment
from ads.forms import CommentForm
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

class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ["title", "price", "text"]
    
class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ["title", "price", "text"]
    
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