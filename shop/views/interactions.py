import json
from boutique.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from shop.models import Product, Like


@login_required
@ajax_required
def like(request, pk):
  data = {}
  product = Product.objects.get(pk=pk)
  is_liked = product.like_set.filter(user=request.user).exists()
  if is_liked:
    product.like_set.filter(user=request.user).delete()
    data['message'] = 'Like'
  else:
    product.like_set.create(user=request.user)
    data['message'] = 'Dislike'
  data['count'] = product.like_set.count()
  return HttpResponse(json.dumps(data), content_type='application/json')