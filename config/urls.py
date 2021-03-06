"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import file.views as file_views
from django.urls import path
from file.views import FileListView, FileCreateView, FileDetailView, FileDownloadView, FileDeleteView, FileExpiryUpdateView, FileRegenerateUrlView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', file_views.HomeView.as_view(), name='home'),
    path('signup/', file_views.signup, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('file/', FileListView.as_view(), name='file-list'),
    path('file/add/', FileCreateView.as_view(), name='file-add'),
    path('file/<str:url>/', FileDownloadView.as_view(), name='file-download'),
    path('file/<str:url>/manage/', FileDetailView.as_view(), name='file-detail'),
    path('file/<str:url>/delete/', FileDeleteView.as_view(), name='file-delete'),
    path('file/<str:url>/update-expiry/', FileExpiryUpdateView.as_view(), name='file-update-expiry'),
    path('file/<str:url>/regenerate/', FileRegenerateUrlView.as_view(), name='file-regenerate-url'),
]
