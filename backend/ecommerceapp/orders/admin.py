from django.contrib import admin
from orders.models import CartItem, Order, OrderItem
# Register your models here.

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
