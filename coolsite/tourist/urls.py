from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TouristHome.as_view(), name='home'),
    path('about/', about, name='about'),# URL адресс арқылы путьті көрсетеді.
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', TouristCategory.as_view(), name='category'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)