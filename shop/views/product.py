import json
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from shop.models import Product, Picture, Boutique
from shop.forms import ProductForm, PictureForm


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.boutique = Boutique.objects.get(pk=self.kwargs['boutique_id'])
        obj.save()
        return super(ProductCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['boutique'] = Boutique.objects.get(pk=self.kwargs['boutique_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['boutique'] = self.get_object().boutique
        return context


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})
        

@login_required
def product_dublicate_view(request, boutique_id, pk):
    data = {}
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        product.id = None
        product.save()
        data = {
            "message": "success",
            "id": product.id
        }
    return JsonResponse(json.dumps(data), safe=False)

@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['pictures'] = self.get_object().picture_set.all()
        return context


@method_decorator(login_required, name='dispatch')
class ProductPictureCreateView(CreateView):
    model = Picture
    form_class = PictureForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.product = Product.objects.get(pk=self.kwargs['product_id'])
        obj.save()
        return super(ProductPictureCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'boutique_id': self.kwargs['boutique_id'], 'pk': self.kwargs['product_id']})