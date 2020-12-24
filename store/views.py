from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from store.models import Product, Category, Customer, Order
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.utils.decorators import method_decorator
# from store.middlewares.auth import auth_middleware
# Create your views here.
def index(request):
    return redirect('product')

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        mobile_number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        value = {
            'first_name':first_name,
            'last_name':last_name,
            'mobile_number':mobile_number,
            'email':email
        }
        error_message = None
        exist_email = Customer.objects.filter(email = email)

        if not first_name:
            error_message = "First name required"
        elif not last_name:
            error_message = "last name is required"
        elif not mobile_number:
            error_message = "Mobile Number is required"
        elif len(mobile_number) < 10:
            error_message = "enter valid mobile number"
        elif not email:
            error_message = "email is required"
        elif not password:
            error_message = "password is required"
        elif exist_email:
            error_message = "mail alredy used"

        if not error_message:
            customer = Customer(first_name = first_name,last_name= last_name,mobile_number = mobile_number,email = email,password = password)
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('product')
        else:
            data = {'error':error_message,'values':value}
            return render(request, 'store/signup.html',data)
    return render(request, 'store/signup.html')


def login(request):
    return_url = None
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        error_message = None
        try:
            customer = Customer.objects.get(email=email)
            if customer:
                password = check_password(password, customer.password)
                if password:
                    request.session['customer_id'] = customer.id
                    request.session['email'] = customer.email
                    if return_url:
                        return HttpResponseRedirect(return_url)
                    else:
                        return_url = None
                        return redirect('product')
                else:
                    error_message = "email and password are not match"
            else:
                error_message = "email and password are not match"
            return render(request, 'store/login.html', {'error':error_message})
        except:
            return render(request, 'store/login.html', {'error': "email and password are not match"})
    return_url = request.GET.get('return_url')
    return render(request, 'store/login.html')

def logout(request):
    request.session.clear()
    return redirect("product")

def product(request):
    if request.method == "GET":
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        product = None  
        categories = Category.get_all_category()
        categoryId = request.GET.get('category')
        if categoryId:
            product = Product.objects.filter(category_id=categoryId)
        else:
            product = Product.objects.all()
        data = {'product':product,'category':categories}
        print(request.session.get('email'))
        return render(request, 'store/product.html', data)
    else:
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quentity = cart.get(product)
            if quentity:
                if remove:
                    if quentity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quentity - 1
                else:
                    cart[product] = quentity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect("product")

def cart(request):
    # print(request.session.get('cart'))
    ids = list(request.session.get('cart').keys())
    product = Product.objects.filter(id__in = ids)
    # print(product)
    return render(request, "store/cart.html", {'products':product})

# @auth_middleware
def checkout(request):
    if request.method == 'POST':
        # print(request.POST)
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        # cart1 = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in = list(cart.keys()))

        for product in products:
            print(type(product.price))
            order = Order(address=address, phone=phone, customer_id=Customer(id = customer), product_id=product, price=product.price, quentity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return redirect('cart')


# @auth_middleware
def order(request):
    customer = request.session.get('customer_id')
    order = Order.objects.filter(customer_id = customer).order_by("-date")
    return render(request, 'store/order.html', {'orders':order})