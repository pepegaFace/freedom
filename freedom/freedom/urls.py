"""freedom URL Configuration

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from academ.yasg_urls import urlpatterns as yasg_urls_academ
import academ.views as academ_views
from kolotok.yasg_urls import urlpatterns as yasg_urls_kolotok
import kolotok.views as views_kolotok
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

"""Academ ViewSets"""
router.register(r'academ/building', academ_views.BuildingViewSet, basename='Building')
router.register(r'academ/apartment', academ_views.ApartmentViewSet, basename='Apartment')
router.register(r'academ/client', academ_views.FixatedClientViewSet, basename='FixatedClient')
router.register(r'academ/favorite', academ_views.FavoritesViewSet, basename='Favorites')
router.register(r'academ/support', academ_views.SupportTicketViewSet, basename='Support')
router.register(r'academ/appointment', academ_views.AppointmentViewSet, basename='Appointment')
router.register(r'academ/reservation', academ_views.ReservationViewSet, basename='Reservation')
router.register(r'academ/gallery', academ_views.ImageGalleryViewSet, basename='Gallery')

router.register(r'auth/users/upload_avatar', academ_views.UploadAvatarViewSet, basename='Upload avatar')

"""Freedom ViewSets"""
router.register(r'freedom/tickets', TicketViewSet, basename='Tickets')

"""Kolotok ViewSets"""
router.register(r'kolotok/products', views_kolotok.ProductViewSet, basename='Products')
router.register(r'kolotok/sub_categories', views_kolotok.SubCategoryViewSet, basename='Sub Categories')
router.register(r'kolotok/categories', views_kolotok.CategoryViewSet, basename='Categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt'))
]

urlpatterns += yasg_urls_kolotok

urlpatterns += yasg_urls_academ

urlpatterns += router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
