from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('add-rating/', views.AddRatingProduct.as_view(), name='add_rating'),
]
