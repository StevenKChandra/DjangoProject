from django.urls import path, reverse_lazy
from . import views

app_name = "ads"
urlpatterns = [
    path("", views.AdListView.as_view(), name="index"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="detail"),
    path("create/", views.AdCreateView.as_view(success_url=reverse_lazy("ads:index")), name="create"),
    path("<int:pk>/update/", views.AdUpdateView.as_view(success_url=reverse_lazy("ads:index")), name="update"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(success_url=reverse_lazy("ads:index")), name="delete"),
]