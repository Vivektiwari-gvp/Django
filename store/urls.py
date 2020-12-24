from django.urls import path
from store import views
from store.middlewares.auth import auth_middleware

urlpatterns = [
    path('', views.index,name='index'),
    path('signup', views.signup,name='signup'),
    path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
    path('product', views.product,name='product'),
    path('cart', views.cart,name='cart'),
    path('checkout', views.checkout,name='checkout'),
    path('order', auth_middleware(views.order),name='order'),
]