import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


from shop.models import Product, Categorie, Type


@login_required
def filter_view(request):
    data = {}

    if request.method == 'POST':
        type = Type.objects.get(pk=request.POST['type_id'])
        categories = Categorie.objects.filter(pk__in=request.POST.getlist('categories[]'))
        products = Product.objects.filter(categorie__in=categories)
        data['products'] = []
        for product in products:
            data['products'].append(product.as_json())

    return JsonResponse(data)


@login_required
def search_view(request):
    if request.method == 'GET':
        term = request.GET['q']
        request.session['term'] = term
        products_list = Product.objects.filter(Q(name__contains=term) | Q(description__contains=term))
        categories = Categorie.objects.all()
        types = Type.objects.all()
        paginator = Paginator(products_list, 10)

        page = request.GET.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {
            'products': products,
            'categories': categories,
            'types': types,
            'term': term
        }

        return render(request, 'shop/search.html', context)