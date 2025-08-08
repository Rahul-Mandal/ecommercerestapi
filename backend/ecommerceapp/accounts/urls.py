from django.urls import path
from .views import RegisterView, LoginView, AdminOnlyView, VendorOnlyView, CustomerOnlyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('vendor-only/', VendorOnlyView.as_view(), name='vendor_only'),
    path('customer-only/', CustomerOnlyView.as_view(), name='customer_only'),
]
