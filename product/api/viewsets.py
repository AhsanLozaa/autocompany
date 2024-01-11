from rest_framework.viewsets import ModelViewSet
from ..models import Product, ShoppingCart, CartItem, Order
from .serializers import OrderSerializer, ProductSerializer, ShoppingCartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.db.models import F

class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ShoppingCartViewset(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        # Check if the user already has a shopping cart
        existing_cart = ShoppingCart.objects.filter(user=user).first()

        if existing_cart:
            # Update the existing cart
            existing_cart.some_field = serializer.validated_data.get('some_field', existing_cart.some_field)
            # Update other fields as needed
            existing_cart.save()
            serializer.instance = existing_cart
        else:
            # Create a new cart
            serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        # Override the create method to handle the response accordingly
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # If a new cart is created, update the response status to 200 OK
            response.status_code = status.HTTP_200_OK
        return response
    
    
    @action(detail=False, methods=['GET'])
    def get_cart_items(self, request):
        user = request.user

        # Get the shopping cart for the user
        shopping_cart = ShoppingCart.objects.filter(user=user).first()

        if not shopping_cart:
            return Response({'detail': 'Shopping cart not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        # Get the cart items for the shopping cart
        cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_user_cart(self, request):
        user = request.user

        # Get the shopping cart for the user
        shopping_cart = ShoppingCart.objects.filter(user=user).first()

        if not shopping_cart:
            return Response({'detail': 'Shopping cart not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShoppingCartSerializer(shopping_cart)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_description="Remove a product from the shopping cart for the authenticated user.")
    @action(detail=False, methods=['POST'])
    def remove_product(self, request):
        user = request.user
        product_id = request.data.get('product_id')

        # Get the shopping cart for the user
        shopping_cart = ShoppingCart.objects.filter(user=user).first()

        if not shopping_cart:
            return Response({'detail': 'Shopping cart not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product exists
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product is in the shopping cart
        cart_item = CartItem.objects.filter(shopping_cart=shopping_cart, product=product).first()
        if not cart_item:
            return Response({'detail': 'Product is not in the shopping cart.'}, status=status.HTTP_404_NOT_FOUND)

        # Remove the specified product from the shopping cart
        cart_item.delete()

        return Response({'detail': 'Product removed from the shopping cart.'}, status=status.HTTP_200_OK)



class CartItemViewset(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
    
    def perform_create(self, serializer):
        user = self.request.user

        # Try to get the user's existing shopping cart
        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        
        print("User:", user)
        print("Existing Shopping Cart:", shopping_cart)

        if not shopping_cart:
            print("Creating new shopping cart")
            # If the user doesn't have a shopping cart, create one
            shopping_cart = ShoppingCart.objects.create(user=user)

        # Auto-add the product to the shopping cart
        product_id = self.request.data.get('product')
        quantity = self.request.data.get('quantity', 1)

        # Check if the product is already in the shopping cart
        cart_item = shopping_cart.cartitem_set.filter(product_id=product_id).first()

        if cart_item:
            # If the product is already in the cart, update the quantity
            print("Updating existing CartItem")
            CartItem.objects.filter(id=cart_item.id).update(quantity=F('quantity') + int(quantity))
        else:
            # If the product is not in the cart, add it as a new item
            print("Creating new CartItem")
            product = get_object_or_404(Product, pk=product_id)
            cart_item = CartItem.objects.create(product=product, shopping_cart=shopping_cart, quantity=quantity)

        # Set the shopping_cart field in the CartItem serializer
        serializer.validated_data['shopping_cart'] = shopping_cart

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     # You can customize this method to include additional logic if needed
    #     serializer.save()

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    
    # @swagger_auto_schema(
    #     operation_description="Create a new order if the current user is the owner of the shopping cart and there are items in the cart.",
    #     request_body=OrderSerializer
    # )
    # @action(detail=False, methods=['POST'])
    def perform_create(self, request):
        user = self.request.user

        # Check if the current user has items in the shopping cart
        shopping_cart = ShoppingCart.objects.filter(user=user).first()

        # Get all the cart items from the cart item table for the reelvant shoppig cart
        cart_items = CartItem.objects.filter(shopping_cart=shopping_cart.id)
        
        
        if not shopping_cart or cart_items.count() <= 0:
            return Response({'detail': 'No items in the shopping cart for the current user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        print("Have Items in the Shoppig cart")
        print(cart_items.count())
        print("Have Items in the Shoppig cart")
        
        # Check if the current user is the owner of the shopping cart
        if shopping_cart.user != user:
            return Response({'detail': 'You are not the owner of the shopping cart.'}, status=status.HTTP_403_FORBIDDEN)

        # Create a new order
        order_data = {
            'shopping_cart': shopping_cart.id,
            'delivery_date': request.data.get('delivery_date'),
            # Other order-related data
        }
        
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            shopping_cart.order_id = order_serializer.instance.id
            shopping_cart.save()

            return Response({'detail': 'Order created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


