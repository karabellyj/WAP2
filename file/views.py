from django.http import FileResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, TemplateView, DeleteView
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


class FileListView(LoginRequiredMixin, ListView):
    template_name = 'file/list.html'
    queryset = File.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class FileCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateFileForm
    template_name = 'file/file_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    slug_url_kwarg = 'url'
    slug_field = 'url_hash'


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    slug_url_kwarg = 'url'
    slug_field = 'url_hash'
    success_url = reverse_lazy('file-list')


class FileDownloadView(View):
    def get(self, request, url):
        file = get_object_or_404(File, url_hash=url)
        response = FileResponse(file.file)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.filename)  # You can set custom filename, which will be visible for clients.
        return response
