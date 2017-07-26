import json
from boutique.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from messenger.models import Notification
from shop.models import Product, Reaction


@login_required
@ajax_required
def react(request, pk):
  data = {}
  product = Product.objects.get(pk=pk)
  reaction = request.GET.get('reaction')
  has_reacted = Reaction.objects.filter(user=request.user, product=product).count() == 1
  reaction_choices = Reaction.get_choices()

  if has_reacted:
    reaction_obj = request.user.reaction_set.get(product=product)
    if reaction in reaction_choices:
      if reaction_obj.type != reaction:
        reaction_obj.type = reaction
        reaction_obj.save()
        
        Notification.send(from_user=request.user, to_user=product.boutique.owner.user, product=product, type=reaction)
      else:
        reaction_obj.delete()
      data['reaction'] = reaction

    elif not reaction:
      reaction_obj.delete()
      data['reaction'] = ''

  elif reaction in  reaction_choices:
    Reaction.objects.create(user=request.user, product=product, type=reaction)

    Notification.send(from_user=request.user, to_user=product.boutique.owner.user, product=product, type=reaction)

    data['reaction'] = reaction;

  data['count'] = product.reaction_set.count()
  return HttpResponse(json.dumps(data), content_type='application/json')
