"""ansimhwajangsil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from store.views import restroom_sign_in_view, loginuser, signupuser, dashboard, viewer_home, private_restroom_form, private_restroom_form_manage, qrgen, logout_view, review

from server.views import error_404_view, qr_scan
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',restroom_sign_in_view, name="restroom_sign_in_view"),
    path("login", loginuser, name='login'),
    path("signup", signupuser, name='signup'),
    path("", viewer_home, name='home'),
    path("settings", private_restroom_form, name="settings"),
    path("error404", error_404_view, name="error"),
    path("api/scan/<str:code>/<str:rc>", qr_scan, name="scan"),
    path("manage/<str:key>", private_restroom_form_manage, name="manage"),
    path("link/<str:code>", qrgen, name="qr"),
    path("logout", logout_view, name="logout"),
    path("review/<str:code>", review, name="review"),
    path("analytics", dashboard, name="dashboard")

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
