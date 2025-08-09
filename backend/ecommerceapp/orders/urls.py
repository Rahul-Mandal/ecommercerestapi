from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = router.urls
