from django.urls import path
from .views import *

from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
	path('', OfferListView.as_view(), name = 'home'),
	path('auth/', LoginRegistrtionView.as_view(), name = 'auth'),
	path('auth/reg/', registration, name = 'auth_reg'),
	path('auth/login/', UserLoginView.as_view(), name = 'auth_login'),
	path('add/', OfferCreateView.as_view(), name = 'add_ad'),
	path('my-ads/', UserOfferListView.as_view(), name = 'my_ads'),
	path('ad/<int:pk>/', UserOfferDetailView.as_view(), name = 'ad'),
	path('ad/change/<int:pk>/', UserOfferUpdateView.as_view(), name = 'ad_change'),
	path('ad/delete/<int:pk>/', UserOfferDeleteView.as_view(), name = 'ad_delete'),
	path('profile/', ProfileView.as_view(), name = 'profile'),
	path('profile/delete/', UserProfileDeleteView.as_view(), name = 'profile_delete'),
	path('logout/', logout_view, name = 'logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)