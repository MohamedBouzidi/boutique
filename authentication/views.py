import json

from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.conf import settings

from shop.models import BusinessUser
from shop.forms import BusinessUserForm

from authentication.models import Profile
from authentication.forms import ProfileForm


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
    return render(request, "authentication/login_register_form.html")


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, password=password, email=email)
                profile = Profile(user=user)
                profile.save()
                return HttpResponseRedirect(reverse_lazy('index'))
    return render(request, "authentication/login_register_form.html")


def business_register_view(request):
    if request.method == 'POST':
        form = BusinessUserForm(request.POST, request.FILES)

        if form.is_valid():
            fields = form.cleaned_data
            businessuser = BusinessUser(description=fields['description'], type=fields['type'])
            businessuser.user = request.user
            request.user.username = request.POST['username']
            request.user.save()
            businessuser.save()
            return render(request, 'shop/boutique_list.html')
        else:
            return render(request, 'authentication/wizard.html', {'form': form})

    return render(request, 'authentication/wizard.html', {'form': BusinessUserForm()})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


@method_decorator(login_required, name='dispatch')
class BusinessUserUpdateView(UpdateView):
    model = BusinessUser
    success_url = reverse_lazy('list_boutique')
    fields = ['description', 'type']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user.username = self.request.POST['username']
        obj.user.save()
        obj.save()
        return super(BusinessUserUpdateView, self).form_valid(form)

    def get_object(self):
        return BusinessUser.objects.get(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class BusinessUserDeleteView(DeleteView):
    model = BusinessUser
    success_url = reverse_lazy('index')

    def get_object(self):
        return BusinessUser.objects.get(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['picture', 'gender']
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):        
        instance = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user.username = request.POST.get('username', obj.user.username)
            obj.picture = request.POST.get('picture')
            obj.user.save()
            obj.save()
            return super(ProfileUpdateView, self).form_valid(form)

        return super(ProfileUpdateView, self).post(request, *args, **kwargs)