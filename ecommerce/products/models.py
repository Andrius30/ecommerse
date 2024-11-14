from django.db import models
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    short_description = models.TextField(blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    group_tag = models.CharField(max_length=200, blank=True, null=True)
    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subcategories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure the slug is unique in the Category table
            counter = 1
            original_slug = self.slug
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class Product(models.Model):
    PRODUCT_STATUS = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('INACTIVE', 'Inactive'),
        ('ACTIVE', 'Active')
    )

    name = models.CharField(max_length=100)
    price = models.FloatField()
    short_description = models.TextField()
    full_description = models.TextField()
    stock = models.IntegerField()
    status = models.CharField(max_length=10, choices=PRODUCT_STATUS, default='INACTIVE')
    discount = models.IntegerField(default=0)
    purchased = models.IntegerField(default=0)
    product_img = models.ImageField(upload_to='products/%Y/%m/%d/')
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if it's empty
            self.slug = slugify(self.name)
            # Ensure the slug is unique in the Product table
            counter = 1
            original_slug = self.slug
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        if self.stock <= 0:
            self.status = 'INACTIVE'
        super().save(*args, **kwargs)
