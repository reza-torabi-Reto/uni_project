from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from .forms import CommentForm
from .models import *
from cart.forms import CartAddProductForm
from star_ratings.models import Rating
from django.db.models import Avg


def index(request):
    most_visited_products = Product.objects.filter(status='p').order_by('-visits')[:5]
    top_rated_products = Product.objects.annotate(avg_rating=Avg('ratings__average')).order_by('-ratings__average')[:5]
    lasted_products = Product.objects.filter(status='p').order_by('-created')[:5]
    context = {
        'most_visited_products': most_visited_products,
        'top_rated_products': top_rated_products,
        'lasted_products': lasted_products,
    }
    return render(request, 'shop/index.html', context= context)

def products(request, slug):
    products = Product.objects.filter(Q(category=get_object_or_404(Category.objects.only('slug'), slug=slug).id))\
        .only('slug', 'name', 'price', 'thumbnail', )
    cate= get_object_or_404(Category.objects.only('title'), Q(slug=slug))
    context = {
        'cate': cate,
        'products': products,
    }
    return render(request, 'shop/products.html', context = context)



def products_category(request, slug): # mobile
    products = Product.objects.filter(category__parent__slug=slug)

    cate= get_object_or_404(Category.objects.only('title'), Q(slug=slug))
    print(f'cate== {cate.title}')
    print(f'cate== {cate.parent}')
    context = {
        'cate': cate,
        'products': products,
    }
    return render(request, 'shop/products-category.html', context = context)


def products_list(request):
    return render(request, 'shop/products-list.html')


# add comment
def product(request, slug):
    product = get_object_or_404(Product, Q(slug=slug) & ~Q(status='h') & ~Q(category__status='h'))
    print(f'prodict->> {product.price}')
    product.visit(request)
    comments = Review.objects.filter(approved_comment=True, product__slug= slug).order_by('-created')
    cart_product_form = CartAddProductForm()
    new_c = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.save()
            new_c = 'ok'

            return render(request, "shop/product.html", {'product': product,
                                                         'comments': comments,
                                                         'new_c': new_c,
                                                         'comment_form': comment_form,
                                                         'cart_product_form': cart_product_form})
    else:
        comment_form = CommentForm()
        return render(request, "shop/product.html", {'product': product,
                                                     'new_c': None,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'cart_product_form': cart_product_form})

    # کد درسافت بیشترین بازدید
    # most_visited_products = Product.objects.annotate(
    #     num_visits=models.Count('visit', distinct=True)
    # ).order_by('-num_visits')[:10]
