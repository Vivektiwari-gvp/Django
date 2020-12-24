from django.contrib import admin
from store.models import Category, Product, Customer, Order
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
	list_display = ('name','price','category_id','description','image')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)