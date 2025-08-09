from rest_framework import viewsets, permissions
from .models import CartItem, Order
from .serializers import CartItemSerializer, OrderSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_items = CartItem.objects.filter(user=self.request.user)
        order = serializer.save(user=self.request.user)
        order.items.set(cart_items)
        cart_items.delete()
