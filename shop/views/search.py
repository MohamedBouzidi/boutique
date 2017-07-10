from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from shop.models import Product, Categorie, Type, Boutique, BusinessUser


@login_required
def search_view(request):
    if request.method == 'GET':
        try:
            categorie_id = int(request.GET.get('c', 0))
            type_id = int(request.GET.get('t', 0))
        except ValueError:
            return HttpResponseRedirect(reverse_lazy('index'))

        search_query = request.GET.get('q', '')
        order_by = request.GET.get('o', 'a')
        price_range = request.GET.get('p', '10,1000')
        price_range_list = price_range.split(',')

        try:
            price_range_int = [int(i) for i in price_range_list]
        except ValueError:
            return HttpResponseRedirect(reverse_lazy('index'))

        price_range_int_ordered = sorted(price_range_int)
        price_min = price_range_int_ordered[0]
        price_max = price_range_int_ordered[1]

        if BusinessUser.objects.filter(user=request.user).exists():
            boutiques = Boutique.objects.exclude(owner=request.user.businessuser)
        else:
            boutiques = Boutique.objects.all()
            
        products_list = Product.objects.filter(
            Q(boutique__in=boutiques),
            Q(active=True),
            Q(price__range=[price_min, price_max])
        )

        categorie = categorie_id or None
        params = ''

        if type_id != 0:
            products_list = products_list.filter(type=Type.objects.get(pk=type_id))
            params = params + 't=' + str(type_id) + '&'

        if categorie_id != 0:
            products_list = products_list.filter(categorie=Categorie.objects.get(pk=categorie_id))
            params = params + 'c=' + str(categorie_id) + '&'

        if not not search_query:
            products_list = products_list.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
            params = params + 'q=' + search_query + '&'

        order_by_string = ''

        # Ordering results
        if order_by == 'le':
            order_by_string = 'price'
        elif order_by == 'me':
            order_by_string = '-price'
        elif order_by == 'lr':
            order_by_string = '-date'
        elif order_by == 'mr':
            order_by_string = 'date'

        if not not order_by_string:
            products_list = products_list.order_by(order_by_string)
            params = params + 'o=' + order_by + '&'

        # Pagination
        paginator = Paginator(products_list, 10)
        page = request.GET.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages) 

        context = {
            'c': categorie,
            'q': search_query,
            'type': type_id,
            'categories': Categorie.objects.all(),
            'types': Type.objects.all(),
            'params': params,
            'products': products
        }

        return render(request, 'shop/search.html', context)