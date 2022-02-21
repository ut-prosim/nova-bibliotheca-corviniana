from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Profile
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

# Create your views here.

@login_required
def account_redirect(request):
    return redirect('profile_view', pk=request.user.profile.id)

class Home(TemplateView):
    template_name = "home.html"
    
@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    model = Profile
    template_name = "profile.html"
    odering = ['date_created']
    
    def get_context_data(self,  **kwargs):
        author = get_object_or_404(Profile, id=self.kwargs['pk'])
        context = super(ProfileView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        context["posts"] = author.posts.all().order_by('-date_created')
        return context
    
class EditProfileView(UpdateView):
    model = Profile
    fields = ['name', 'image', 'current_city']
    template_name = 'editprofile.html'
    def get_success_url(self):
        print(self.kwargs)
        return reverse('profile_view', kwargs={'pk': self.object.pk})

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'createprofile.html'
    fields = ['name', 'image', 'current_city']
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, 'registration/signup.html', context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/createprofile/')
        else:
            context = {'form': form}
            return render(request, 'registration/signup.html', context)
        
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    def get(self, request):
        form = UserChangeForm()
        context = {"form": form}
        return render(request, 'registration/profile_update.html', context)
    def get_object(self):
        return self.request.user