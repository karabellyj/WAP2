import io
import mimetypes
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

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
        # uploaded_file = form.files['data']


        form.instance.user = self.request.user
        return super().form_valid(form)


class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    slug_url_kwarg = 'url'
    slug_field = 'url_hash'


class FileDownloadView(View):
    def get(self, request, url):
        file = get_object_or_404(File, url_hash=url)
        # mime = mimetypes.guess_type(file.file.name)[0]
        response = FileResponse(file.file)
        # response['Content-Type'] = mimetypes
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.filename)  # You can set custom filename, which will be visible for clients.
        return response
