import json
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from boutique.decorators import ajax_required

from shop.models import Product, Picture, Boutique, BusinessUser
from shop.forms import ProductForm, PictureForm


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductCreateView, self).post(request, *args, **kwargs)

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
    fields = ['name', 'price', 'image', 'description', 'active', 'quantite', 'categorie', 'type']

    def get(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))

        instance = Product.objects.get(pk=kwargs['pk'])
        form = ProductForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            print(instance.__dict__)
            return super(ProductUpdateView, self).form_valid(form)

        return super(ProductUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['boutique'] = self.get_object().boutique
        return context


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product

    def get(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})
        

@login_required
def product_dublicate_view(request, boutique_id, pk):
    data = {}
    
    product = Product.objects.get(pk=pk)
    if request.user != product.boutique.owner.user:
        return HttpResponseRedirect(reverse_lazy('index'))
    
    if request.method == 'POST':
        product.id = None
        product.date = None
        product.save()
        data = {
            "id": product.id,
            "boutique_id": product.boutique.id,
            "active": product.active
        }
    return JsonResponse(json.dumps(data), safe=False)

@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        is_owner = BusinessUser.objects.filter(user=request.user).exists() and self.get_object().boutique.owner == request.user.businessuser
        if not is_owner and not self.get_object().active:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['pictures'] = self.get_object().picture_set.all()
        has_businessuser = BusinessUser.objects.filter(user=self.request.user).exists()
        if has_businessuser and self.get_object().boutique.owner == self.request.user.businessuser:
            context['is_owner'] = True 
        return context


@method_decorator(login_required, name='dispatch')
class ProductPictureCreateView(CreateView):
    model = Picture
    form_class = PictureForm

    def get(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductPictureCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductPictureCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.product = Product.objects.get(pk=self.kwargs['product_id'])
        obj.save()
        return super(ProductPictureCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'boutique_id': self.kwargs['boutique_id'], 'pk': self.kwargs['product_id']})


@method_decorator(login_required, name='dispatch')
class ProductPictureUpdateView(UpdateView):
    model = Picture
    form_class = PictureForm

    def get(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductPictureUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductPictureUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.product = Product.objects.get(pk=self.kwargs['product_id'])
        obj.save()
        return super(ProductPictureUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'boutique_id': self.kwargs['boutique_id'], 'pk': self.kwargs['product_id']})


@method_decorator(login_required, name='dispatch')
class ProductPictureDeleteView(DeleteView):
    model = Picture

    def get(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductPictureDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['boutique_id'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(ProductPictureDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'boutique_id': self.kwargs['boutique_id'], 'pk': self.kwargs['product_id']})


@login_required
def product_state_view(request, boutique_id, pk):
    product = Product.objects.get(pk=pk)
    
    if request.user != product.boutique.owner.user:
        return HttpResponseRedirect(reverse_lazy('index'))

    if request.method == 'POST':
        product.active = not product.active
        product.save()

    data = {
        "active": product.active
    }

    return JsonResponse(json.dumps(data), safe=False)


@ajax_required
@login_required
def product_list_view(request, boutique_id):
    query = request.GET.get('query')
    page = request.GET.get('page')
    boutique = Boutique.objects.get(pk=boutique_id)

    if not not query:
        product_list = Product.objects.filter(name__icontains=query, boutique=boutique)
    else:
        product_list = Product.objects.filter(boutique=boutique)

    paginator = Paginator(product_list, 3)

    try:
        page = int(page)
    except ValueError:
        print('page not an integer')
        page = 1

    if page > paginator.num_pages:
        page = 1

    if page < 1:
        page = paginator.num_pages 

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'partials/product_list.html', {'products': products, 'page': page})