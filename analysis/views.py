from django.db.models import Sum
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone
from django.views import View

from analysis.models import ProductStatistic
from shop.models import Product


