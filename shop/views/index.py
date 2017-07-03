from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from shop.models import Boutique, Product, Categorie, Type

@method_decorator(login_required, name='dispatch')
class IndexView(ListView):
    model = Product
    template_name = "shop/index.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        boutiques = Boutique.objects.exclude(owner=self.request.user)
        return Product.objects.filter(boutique__in=boutiques).filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        context['types'] = Type.objects.all()
        context['rows'] = range(0, self.get_queryset().count(), 3)
        return context