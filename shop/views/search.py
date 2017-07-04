import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core import serializers
from django.db.models import Q

from shop.models import Product, Categorie, Type


@login_required
def get_search_results(request):
    context = { 
        "categories": Categorie.objects.all(),
        "types": Type.objects.all()
    }

    if request.method == 'POST':
        categorie_ids = request.POST.getlist('categories[]')
        price = request.POST['price']

        categories = Categorie.objects.filter(pk__in = categorie_ids)
        context["products"] = Product.objects.filter(categorie__in = categories).order_by('-date')


    return render(request, 'shop/index.html', context)
