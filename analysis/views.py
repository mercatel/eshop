from django.http import HttpResponse

from django.views import View

from analysis.forms import RatingForm
from analysis.models import RatingProduct
from shop.utils import get_client_ip


class AddRatingProduct(View):

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            RatingProduct.objects.update_or_create(
                ip=get_client_ip(request),
                product_id=int(request.POST.get('product')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
