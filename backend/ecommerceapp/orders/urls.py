from django.urls import path
from .views import AddToCartView, OrderViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'order', OrderViewSet, basename='order')

# urlpatterns = router.urls

urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('order/', OrderViewSet.as_view(), name='order')
]