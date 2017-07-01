from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Boutique, Product, BusinessUser


class IndexView(ListView):
    model = Product
    template_name = "shop/index.html"
    context_object_name = "products"
    paginate_by = 10