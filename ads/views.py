from django.views import generic
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime

from ads.owner import OwnerDeleteView
from ads.models import Ad, Comment, Fav
from ads.forms import CommentForm, CreateForm
# Create your views here.

class AdListView(View):
    template_name = "ads/ad_list.html"

    def get(self, request):
        search_key = request.GET.get("search", False)

        if search_key:
            query = Q(title__icontains=search_key)
            query.add(Q(description__icontains=search_key), Q.OR)
            query.add(Q(tags__name__in=[search_key]), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().distinct().order_by("-updated_at")[:10]
        else:
            ad_list = Ad.objects.all().order_by("-updated_at")[:10]
        
        for ad in ad_list:
            ad.natural_updated = naturaltime(ad.updated_at)

        fav = []
        if request.user.is_authenticated:
            rows = request.user.favourite_ads.values("id")
            fav = [row["id"] for row in rows]
        
        context = {"ad_list": ad_list, "favourites": fav}
        return render(request, self.template_name, context)

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
    success_url = reverse_lazy("ads:index")
    
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
        form.save_m2m() # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false

        return redirect(self.success_url)

    
class AdUpdateView(LoginRequiredMixin, View):
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:index")
    
    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        context = {"form": CreateForm(instance=ad)}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            context = {"form": form}
            return render(request, self.template_name, context)

        ad = form.save(commit=False)
        ad.save()
        form.save_m2m() # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false

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

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
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

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name="dispatch")
class FavouriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(user = self.request.user, ad=ad)
        try:
            fav.save()
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class UnfavouriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=self.request.user, ad=ad).delete()
        except Fav.DoesNotExist as e:
            pass
        return HttpResponse()
