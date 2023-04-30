"""coolsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin

from coolsite import settings
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from tourist.views import TouristAPIView
from tourist.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/tourist/', TouristAPIList.as_view()),
    path('api/v1/tourist/<int:pk>/', TouristAPIUpdate.as_view()),
    path('api/v1/touristdelete/<int:pk>/', TouristAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('captcha/', include('captcha.urls')),
    path('', include('tourist.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound