from django.urls import path, reverse_lazy
from . import views

app_name = "ads"
urlpatterns = [
    path("", views.AdListView.as_view(), name="index"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="detail"),
    path("ad/create/", views.AdCreateView.as_view(success_url=reverse_lazy("ads:index")), name="create"),
    path("ad/<int:pk>/update/", views.AdUpdateView.as_view(success_url=reverse_lazy("ads:index")), name="update"),
    path("ad/<int:pk>/delete/", views.AdDeleteView.as_view(success_url=reverse_lazy("ads:index")), name="delete"),
    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
    path("comment/<int:pk>/create/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),
]