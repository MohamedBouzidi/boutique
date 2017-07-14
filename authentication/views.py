from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView

from authentication.forms import SignUpForm, ProfileForm
from authentication.models import Profile
from feeds.models import Feed


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            welcome_post = '{0} has joined the network.'.format(user.username,
                                                                user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()
            return redirect('/')

    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm()})



@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    model = Profile
    success_url = reverse_lazy('index')
    fields = ['picture', 'gender']

    def get_object(self):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):        
        instance = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user.username = self.request.POST.get('username')
            obj.user.save()
            obj.save()
            return super(UserProfileUpdateView, self).form_valid(form)
        return super(UserProfileUpdateView, self).post(request, *args, **kwargs)