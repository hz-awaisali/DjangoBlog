from django.urls import path
from .views import *

urlpatterns = [
    # path('', blogs, name='blogs'),
    path('<int:bid>', detailed_blog, name='detailed_blog'),
]
