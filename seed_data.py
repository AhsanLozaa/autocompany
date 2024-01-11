import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autocompany.settings')
django.setup()


from django.contrib.auth import get_user_model
from product.models import Product, ShoppingCart, CartItem, Order
from faker import Faker
import random


fake = Faker()
User = get_user_model()

def seed_shopping_cart():
    # Create 10 users
    users = []
    for _ in range(10):
        user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password=fake.password())
        users.append(user)

    # Create 100 products
    products = []
    for _ in range(100):
        product = Product.objects.create(
            name=fake.word(),
            description=fake.text(),
            price=random.uniform(5.0, 100.0)
        )
        products.append(product)

    # Create a shopping cart for each user and add random products
    for user in users:
        shopping_cart = ShoppingCart.objects.create(user=user)

        # Add random products to the shopping cart
        for _ in range(random.randint(1, 10)):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            CartItem.objects.create(product=product, shopping_cart=shopping_cart, quantity=quantity)

        # Create an order associated with the shopping cart
        order = Order.objects.create(shopping_cart=shopping_cart, delivery_date=fake.future_datetime(end_date='+30d'))

        # Display information
        print(f"User: {user}")
        print(f"Shopping Cart: {shopping_cart}")
        print(f"Products in Cart: {shopping_cart.products.all()}")
        print(f"Order: {order}")

if __name__ == '__main__':
    seed_shopping_cart()
