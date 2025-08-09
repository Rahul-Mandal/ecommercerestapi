from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from accounts.permissions import IsAdmin, IsVendor, IsCustomer
from rest_framework.permissions import AllowAny,IsAuthenticated

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

