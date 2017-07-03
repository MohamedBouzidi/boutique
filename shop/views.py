import json
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core import serializers

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Boutique, Product, BusinessUser, Categorie
from .forms import BoutiqueForm, ProductForm


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
        context['rows'] = range(0, self.get_queryset().count(), 3)
        return context


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.boutique = Boutique.objects.get(pk=self.kwargs['boutique_id'])
        obj.save()
        return super(ProductCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse_lazy('detail_boutique', kwargs={'pk': self.kwargs['boutique_id']})
        

@login_required
def product_dublicate_view(request, boutique_id, pk):
    product = Product.objects.get(pk=pk)
    product.id = None
    product.save()
    return HttpResponseRedirect(reverse_lazy('edit_product', kwargs={'boutique_id': product.boutique.id, 'pk': product.id}))


@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


@method_decorator(login_required, name='dispatch')
class BoutiqueListView(ListView):
    model = Boutique
    context_object_name = 'boutiques'
    paginate_by = 10

    def get_queryset(self):
        boutiques = Boutique.objects.filter(owner=self.request.user).order_by('-date')
        return boutiques


@method_decorator(login_required, name='dispatch')
class BoutiqueCreateView(CreateView):
    model = Boutique
    success_url = reverse_lazy('index')
    form_class = BoutiqueForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super(BoutiqueCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class BoutiqueDetailView(DetailView):
    model = Boutique
    context_object_name = 'boutique'

    def get_context_data(self, **kwargs):
        context = super(BoutiqueDetailView, self).get_context_data(**kwargs)
        context['products'] = self.get_object().product_set.order_by('-date')
        return context


@method_decorator(login_required, name='dispatch')
class BoutiqueUpdateView(UpdateView):
    model = Boutique
    success_url = reverse_lazy('index')
    form_class = BoutiqueForm


@method_decorator(login_required, name='dispatch')
class BoutiqueDeleteView(DeleteView):
    model = Boutique
    success_url = reverse_lazy('index')


@login_required
def search_view(request):
    if request.method == 'GET':
        categorie_id = request.GET['categorie_id']
        products = Product.objects.filter(categorie=Categorie.objects.get(pk=categorie_id))
        data = {
            'products': serializers.serialize('json', products)
        }
        return HttpResponse(JsonResponse(data), content_type="application/json")


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).count() > 0:
            username = User.objects.filter(email=email).first().username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('index'))
    return render(request, "shop/login_register_form.html")


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, password=password, email=email)
                return HttpResponseRedirect(reverse_lazy('index'))
    return render(request, "shop/login_register_form.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))