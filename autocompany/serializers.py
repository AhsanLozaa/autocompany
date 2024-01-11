# serializers.py

from rest_framework import serializers
from .models import Product, SampleTable, ShoppingCart, Order
from rest_framework.schemas import AutoSchema

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ShoppingCartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class SampleTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleTable
        fields = ['name', 'description']



