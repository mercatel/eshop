from django.shortcuts import render

# Create your views here.
from dashboard.forms import ProductForm


def dashboard(request):
    form = ProductForm
    return render(request, 'test.html', context={'form': form})
