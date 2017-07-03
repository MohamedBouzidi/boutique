from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from shop.models import Product, Categorie


@login_required
def search_view(request):
    if request.method == 'GET':
        categorie_id = request.GET['categorie_id']
        products = Product.objects.filter(categorie=Categorie.objects.get(pk=categorie_id))
        data = {
            'products': serializers.serialize('json', products)
        }
        return HttpResponse(JsonResponse(data), content_type="application/json")