"""
URL configuration for wow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic.base import TemplateView
from core.views import home, ProfileView, send_email_to_every_user
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as email_urls
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('post/', include('core.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    #path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    path('email/', include(email_urls), name='email-verification'),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('sendmail/', send_email_to_every_user, name = 'send_email_to_every_user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
