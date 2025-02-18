"""
URL configuration for DjangoBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from blogs.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('logout/', logout_user, name='logout_user'),
    path('create/', create_blog, name='create_blog'),
    path('update/', update_blogs_list, name='update_blogs_list'),
    path('update/<int:bid>/', update_blog, name='update_blog'),
    path('delete/<int:bid>/', delete_blog, name='delete_blog'),


    path('blogs/', include('blogs.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
