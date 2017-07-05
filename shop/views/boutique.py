from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from shop.models import Boutique, BusinessUser
from shop.forms import BoutiqueForm


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

    def get_context_data(self, **kwargs):
        context = super(BoutiqueCreateView, self).get_context_data(**kwargs)
        context['new_businessuser'] = BusinessUser.objects.filter(user=self.request.user).count() == 0
        return context

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