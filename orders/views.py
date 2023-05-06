from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    print(f'---------One')
    cart = Cart(request)
    if request.method == 'POST':
        print('---------two')
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            print('tree')
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                             product=item['product'],
                             price=item['price'],
                             quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request,'orders/order/created.html',{'order': order})
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html', {'cart': cart, 'form': form})
