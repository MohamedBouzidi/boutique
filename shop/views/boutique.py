from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from shop.models import Boutique, BusinessUser
from shop.forms import BoutiqueForm


@method_decorator(login_required, name='dispatch')
class BoutiqueListView(ListView):
    model = Boutique
    context_object_name = 'boutiques'
    template_name = 'shop/boutique_list.html'
    paginate_by = 10

    def get_queryset(self):
        has_businessuser = BusinessUser.objects.filter(user=self.request.user).exists()
        if has_businessuser:
            boutiques = Boutique.objects.filter(owner=self.request.user.businessuser).order_by('-date')
        else:
            boutiques = []
        return boutiques


@method_decorator(login_required, name='dispatch')
class BoutiqueCreateView(CreateView):
    model = Boutique
    success_url = reverse_lazy('list_boutique')
    form_class = BoutiqueForm

    def get_context_data(self, **kwargs):
        context = super(BoutiqueCreateView, self).get_context_data(**kwargs)
        context['new_businessuser'] = BusinessUser.objects.filter(user=self.request.user).count() == 0
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = BusinessUser.objects.get(user=self.request.user)
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

    def get(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['pk'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(BoutiqueUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['pk'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(BoutiqueUpdateView, self).post(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class BoutiqueDeleteView(DeleteView):
    model = Boutique
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        boutique = Boutique.objects.get(pk=kwargs['pk'])
        if request.user != boutique.owner.user:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super(BoutiqueDeleteView, self).post(request, *args, **kwargs)