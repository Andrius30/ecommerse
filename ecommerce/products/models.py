from django.db import models


# Create your models here.
class Product(models.Model):
    PRODUCT_STATUS = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('INACTIVE', 'Inactive'),
        ('ACTIVE', 'Active')
    )
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    status = models.CharField(max_length=10, choices=PRODUCT_STATUS, default='INACTIVE')
    discount = models.IntegerField(default=0)
    purchased = models.IntegerField(default=0)
    product_img = models.ImageField(upload_to='products/%Y/%m/%d/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.stock <= 5:
            self.status = 'INACTIVE'
        super().save(*args, **kwargs)
