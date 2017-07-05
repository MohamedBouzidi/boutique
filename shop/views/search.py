from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


from shop.models import Product, Categorie, Type


@login_required
def search_view(request):
    if request.method == 'GET':
        try:
            categorie_id = int(request.GET.get('c', 0))
        except ValueError:
            return HttpResponseRedirect(reverse_lazy('index'))


        search_query = request.GET.get('q', '')

        products_list = None

        context = {
            'categories': Categorie.objects.all(),
            'types': Type.objects.all(),
            'params': {}
        }

        if categorie_id != 0:
            products_list = Product.objects.filter(categorie=Categorie.objects.get(pk=categorie_id))
            context['params']['c'] = categorie_id

        if not not search_query:
            if not products_list:
                products_list = Product.objects
            products_list = products_list.filter(Q(name__contains=search_query) | Q(description__contains=search_query))
            context['params']['q'] = search_query

        paginator = Paginator(products_list, 10)
        page = request.GET.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['products'] = products

        return render(request, 'shop/search.html', context)