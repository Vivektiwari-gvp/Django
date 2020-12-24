from django.db import models
import datetime
# Create your models here.

class Customer(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	mobile_number = models.CharField(max_length=15)
	email = models.EmailField()
	password = models.CharField(max_length=500)


class Category(models.Model):
	name = models.CharField(max_length=300)

	@staticmethod
	def get_all_category():
		return Category.objects.all()

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=300)
	price = models.IntegerField(default=0)
	category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
	description = models.CharField(max_length=300)
	image = models.ImageField(upload_to='product/')

class Order(models.Model):
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quentity = models.IntegerField(default=1)
	price = models.IntegerField()
	address = models.CharField(max_length=50, default='', blank=True)
	phone = models.CharField(max_length=50, default='', blank=True)
	date = models.DateTimeField(default=datetime.datetime.today) 
	status = models.BooleanField(default=False)