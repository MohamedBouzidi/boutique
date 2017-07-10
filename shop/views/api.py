import json
from django.http import JsonResponse

from shop.models import Product

def products_api_view(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        return JsonResponse(json.dumps(product.as_json()), safe=False)