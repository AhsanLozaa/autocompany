from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # class Meta:
    #     app_label = 'autocompany'

class ShoppingCart(models.Model):
    user_id = models.IntegerField()  # Assuming a simple user identifier for now
    products = models.ManyToManyField(Product)

    # class Meta:
    #     app_label = 'autocompany'

class Order(models.Model):
    user_id = models.IntegerField()
    products = models.ManyToManyField(Product)
    delivery_date = models.DateTimeField()

    # class Meta:
    #     app_label = 'autocompany'

# class SampleTable(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     # class Meta:
#     #     app_label = 'autocompany'

class SampleTable(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    # def __str__(self):
    #     return self.name
