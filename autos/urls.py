from django.urls import path
from . import views

app_name = 'autos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('main/create/', views.AutoCreate.as_view(), name='auto_create'),
    path('main/<int:pk>/update/', views.AutoUpdate.as_view(), name='auto_update'),
    path('main/<int:pk>/delete/', views.AutoDelete.as_view(), name='auto_delete'),
    path('lookup/', views.ManufacturerView.as_view(), name='manufacturer_list'),
    path('lookup/create/', views.ManufacturerCreate.as_view(), name='manufacturer_create'),
    path('lookup/<int:pk>/update/', views.ManufacturerUpdate.as_view(), name='manufacturer_update'),
    path('lookup/<int:pk>/delete/', views.ManufacturerDelete.as_view(), name='manufacturer_delete'),
]
