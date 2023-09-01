"""
URL configuration for CasaLeiloes project.

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
from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'CasaLeiloes'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('dashboard/', views.adminDashboard, name='admin'),
    path('register/', views.registration, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('edit_perfil/<int:user_id>/', views.edit_perfil, name='edit_perfil'),
    path('password_change/', views.password_change, name='password_change'),
    path('watchlist/<int:auction_id>/', views.watchlist, name='watchlist'),
    path('add_item/', views.add_item, name='add_item'),
    path('alter_produto/<int:product_id>/', views.alter_produto, name='alter_produto'),
    path('add_auction/', views.add_auction, name='add_auction'),
    path('alter_auction/<int:auction_id>/', views.alter_auction, name='alter_auction'),
    path('bid/<int:bid_id>/', views.bid, name='bid'),
    path('products/', views.product_list, name='product_list'),
    path('negociacoes/', views.negociacoes_list, name='negociacoes'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)