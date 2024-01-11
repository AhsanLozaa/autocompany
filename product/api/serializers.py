from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from ..models import Product, ShoppingCart, CartItem, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'created_at',
            'updated_at'
        ]

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = [
            'products',
            'created_at',
            'updated_at'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'product',
            # 'shopping_cart',
            'quantity',
            'created_at',
            'updated_at'
        ]
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'shopping_cart',
            'delivery_date',
            'order_date',
            'created_at',
            'updated_at'
        ]