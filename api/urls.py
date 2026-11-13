from django.urls import path
from .views import vendors_create, vendor_detail, items_create, item_detail, organizers_create, organizer_detail, malls_create, mall_detail, markets_create, market_detail, booths_create, booth_detail, bookings_create, booking_detail, invoices_create, invoice_detail
from api.views import LoginView, LogoutView

urlpatterns = [
    path('vendors/', vendors_create, name='vendors_create'),
    path('vendors/<str:pk>/', vendor_detail, name='vendor_detail'),
    path('items/', items_create, name='items_create'),
    path('items/<str:pk>/', item_detail, name='item_detail'),
    path('organizers/', organizers_create, name='organizers_create'),
    path('organizers/<str:pk>/', organizer_detail, name='organizer_detail'),
    path('malls/', malls_create, name='malls_create'),
    path('malls/<str:pk>/', mall_detail, name='mall_detail'),
    path('markets/', markets_create, name='markets_create'),
    path('markets/<str:pk>/', market_detail, name='market_detail'),
    path('booths/', booths_create, name='booths_create'),
    path('booths/<str:pk>/', booth_detail, name='booth_detail'),
    path('bookings/', bookings_create, name='bookings_create'),
    path('bookings/<str:pk>/', booking_detail, name='booking_detail'),
    path('invoices/', invoices_create, name='invoices_create'),
    path('invoices/<str:pk>/', invoice_detail, name='invoice_detail'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]