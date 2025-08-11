from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from .models import CartItem, Order
from .serializers import CartItemSerializer, OrderSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         cart_items = CartItem.objects.filter(user=self.request.user)
#         order = serializer.save(user=self.request.user)
#         order.items.set(cart_items)
#         cart_items.delete()

# class OrderViewSet(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         cart_items = CartItem.objects.filter(user=request.user)
#         if not cart_items.exists():
#             return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ First: Create and save the order
#         order = Order.objects.create(user=request.user)

#         # ✅ Then: Add items to order
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.price
#             )

#         # ✅ Now it's safe to calculate total
#         order.total_price = order.calculate_total()
#         order.save()

#         cart_items.delete()

#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class OrderViewSet(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         cart_items = CartItem.objects.filter(user=user)

#         if not cart_items.exists():
#             return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ 1. Save order first so it gets a primary key (ID)
#         order = Order.objects.create(user=user)

#         # ✅ 2. Add items to the order
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.price  # store price at order time
#             )

#         # ✅ 3. Calculate total price AFTER adding items
#         order.total_price = sum(item.product.price * item.quantity for item in cart_items)
#         order.save()

#         # ✅ 4. Clear the cart
#         cart_items.delete()

#         # ✅ 5. Return the created order
#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


from django.db import transaction

# class OrderViewSet(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         cart_items = CartItem.objects.filter(user=user)

#         if not cart_items.exists():
#             return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

#         with transaction.atomic():
#             order = Order.objects.create(user=user)

#             total = 0
#             for item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                     price=item.product.price
#                 )
#                 total += item.product.price * item.quantity

#             order.total_price = total
#             order.save()

#             cart_items.delete()

#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.select_related('product').filter(user=user)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # ✅ Create and SAVE the order first
            order = Order.objects.create(user=user)

            total = 0
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                total += item.product.price * item.quantity

            # ✅ Save total price
            order.total_price = total
            order.save()

            # ✅ Clear cart
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# orders/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404

from products.models import Product
from .models import CartItem
from .serializers import AddToCartSerializer

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        product = get_object_or_404(Product, id=product_id)

        # Check if item is already in cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            # Already in cart: update quantity
            cart_item.quantity += quantity
        else:
            # New item: set quantity
            cart_item.quantity = quantity

        cart_item.save()

        return Response({
            'message': 'Product added to cart',
            'product_id': product.id,
            'quantity': cart_item.quantity
        }, status=status.HTTP_200_OK)
