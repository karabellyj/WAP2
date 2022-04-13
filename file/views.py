from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from file.models import File
from .forms import CreateFileForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'file/register.html', {'form': form})


class HomeView(TemplateView):
    template_name = 'file/home.html'


class FileView(TemplateView):
    template_name = 'file_view.html'
    model = File


class FileCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateFileForm
    template_name = 'file/file_form.html'

    def form_valid(self, form):
        # uploaded_file = form.files['file'].file
        # data = uploaded_file.file.read()
        
        form.instance.user = self.request.user
        return super().form_valid(form)


class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    