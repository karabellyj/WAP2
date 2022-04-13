from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.views import View
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


class FileListView(ListView):
    template_name = 'file/list.html'
    queryset = File.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

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
    slug_url_kwarg = 'url'
    slug_field = 'url_hash'


class FileDownloadView(View):
    pass
