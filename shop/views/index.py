from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from shop.models import Boutique, Product, Categorie, Type, BusinessUser

@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Product
    template_name = "shop/index.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        has_businessuser = BusinessUser.objects.filter(user=self.request.user).exists()
        if has_businessuser:
            boutiques = Boutique.objects.exclude(owner=self.request.user.businessuser)
        else:
            return Product.objects.filter(active=True)
        return Product.objects.filter(boutique__in=boutiques).filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        categorie_list = Categorie.objects.all()
        categories = []
        for categorie in categorie_list:
            if categorie.product_set.count():
                categories.append(categorie)

        context['categories'] = categories
        context['types'] = Type.objects.all()
        context['rows'] = range(0, self.get_queryset().count(), 3)
        return context