from django.urls import path, include
from rest_framework.routers import SimpleRouter

# from post.api import viewsets, views
from ..api import views, viewsets

router = SimpleRouter()
router.register(r'product', viewsets.ProductViewset, basename='product',)
router.register(r'shopping-cart', viewsets.ShoppingCartViewset, basename='shoppingcart')
router.register(r'cart-item', viewsets.CartItemViewset, basename='cartitem')
router.register(r'order', viewsets.OrderViewset, basename='order')
# router.register(r'comments', viewsets.CommentViewset, basename='comment')


urlpatterns = [
    path('ping/', views.PingView.as_view(), name='ping'),
] + router.get_urls()