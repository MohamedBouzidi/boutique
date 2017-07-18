import json
from boutique.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from shop.models import Product, Reaction


@login_required
@ajax_required
def react(request, pk):

  data = {}
  product = Product.objects.get(pk=pk)
  reaction = request.GET.get('reaction')
  has_reacted = Reaction.objects.filter(user=request.user, product=product).count() == 1
  reaction_choices = Reaction.get_choices()

  print(reaction_choices)

  if has_reacted:
    print('has reacted')
    reaction_obj = request.user.reaction_set.filter(product=product).first()
    if reaction in reaction_choices:
      reaction_obj.type = reaction
      reaction_obj.save()
      data['reaction'] = reaction

      if reaction == reaction_obj.type:
        reaction_obj.delete()

    elif not reaction:
      reaction_obj.delete()
      data['reaction'] = ''

  elif reaction in  reaction_choices:
    Reaction.objects.create(user=request.user, product=product, type=reaction)
    data['reaction'] = reaction;

  data['count'] = product.reaction_set.count()
  return HttpResponse(json.dumps(data), content_type='application/json')
