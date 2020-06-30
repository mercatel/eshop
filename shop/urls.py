from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('product_list/', views.ProductView.as_view(), name='product_list'),
    path('search/', views.Search.as_view(), name='search'),
    path('<slug:slug>/', views.ProductDetailView1.as_view(), name='product_detail'),

]
