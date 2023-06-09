from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from .forms import CommentForm
from .models import *
from cart.forms import CartAddProductForm
from star_ratings.models import Rating
from django.db.models import Avg
from django.db.models import Sum
from .recommender import Recommender
from .filters import ProductFilter
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger



def index(request):
    products = Product.objects.filter(is_active=True)
    most_visited_products = products.order_by('-visits')[:5]
    top_rated_products = products.annotate(avg_rating=Avg('ratings__average')).order_by('-ratings__average')[:5]
    lasted_products = products.order_by('-created')[:5]
    special_products = products.filter(~Q(special = 0)).order_by('-created')[:5]
    best_selling_products = products.annotate(total_sales=Sum('order_items__quantity')).order_by('-total_sales')[:5]

    context = {
        'most_visited_products': most_visited_products,
        'top_rated_products': top_rated_products,
        'lasted_products': lasted_products,
        'best_selling_products': best_selling_products,
        'special_products': special_products,
    }
    return render(request, 'shop/index.html', context= context)


# from django.views.generic import ListView
#
# class ProductsCategory(ListView):
#     model = Product
#     template_name = 'shop/products-category.html'
#     context_object_name = 'list'
#     paginate_by = 10
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(is_active=True)
#         sort_by = self.request.GET.get('sort')
#         min_price = self.request.GET.get('min_price')
#         max_price = self.request.GET.get('max_price')
#         print(f'MaxP= {max_price}')
#
#         if sort_by == 'price_asc':
#             queryset = queryset.order_by('price')
#         elif sort_by == 'price_desc':
#             queryset = queryset.order_by('-price')
#         elif sort_by == 'sales':
#             queryset = queryset.annotate(total_sales=Sum('order_items__quantity')).order_by('-total_sales')
#         elif sort_by == 'visits':
#             queryset = queryset.order_by('-visits')
#         elif sort_by == 'stars':
#             queryset = queryset.annotate(avg_rating=Avg('ratings__average')).order_by('-ratings__average')
#
#         if max_price and min_price:
#             queryset = queryset.filter(Q(Q(price__gte=min_price) | Q(price__lte=max_price)))
#         if min_price :
#             queryset = queryset.filter(price__gte=min_price)
#         if max_price:
#             queryset = queryset.filter(price__lte=max_price)
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['sort_by'] = self.request.GET.get('sort_by', '')
#         context['min_price'] = self.request.GET.get('min_price', '')
#         context['max_price'] = self.request.GET.get('max_price', '')
#         return context

def products_category(request, slug): # mobile
    cate = get_object_or_404(Category.objects.only('title'), Q(slug=slug))
    queryset = Product.objects.filter(category__parent__slug=slug, is_active=True)
    sort_by = request.GET.get('sort')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    s = Product.sort_products(Product, queryset, sort_by, min_price, max_price)
    if s:
        queryset = s

    # Pagination
    paginator = Paginator(queryset, 2)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'cate': cate,
        'list': page_obj,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
            }
    return render(request, 'shop/products-category.html', context=context)


def products(request, slug):
    cate = get_object_or_404(Category.objects.only('title'), Q(slug=slug))
    queryset = Product.objects.filter(Q(category=get_object_or_404(Category.objects.only('slug'), slug=slug).id)) \
        .only('slug', 'name', 'price', 'thumbnail', )

    sort_by = request.GET.get('sort')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    print(f'--------Max= {max_price}, {min_price}')
    s = Product.sort_products(Product, queryset, sort_by, min_price, max_price)
    if s:
        queryset = s

    # Pagination
    paginator = Paginator(queryset, 2)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'cate': cate,
        'list': page_obj,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'shop/products.html', context=context)




def products_list(request):
    return render(request, 'shop/products-list.html')


# add comment
def product(request, slug):
    product = get_object_or_404(Product, Q(slug=slug) & ~Q(status='h') & ~Q(category__status='h'))
    product.visit(request)
    comments = Review.objects.filter(approved_comment=True, product__slug= slug).order_by('-created')
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 5)
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
                                                         'cart_product_form': cart_product_form,
                                                         'recommended_products':recommended_products})
    else:
        comment_form = CommentForm()
        return render(request, "shop/product.html", {'product': product,
                                                     'new_c': None,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'cart_product_form': cart_product_form,
                                                     'recommended_products':recommended_products })


def search(request):
    if request.method == 'GET' and request.GET.get('q'):
        search_item = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if search_item:
            context = {
                'products':Product.objects.filter(Q(Q(name__icontains=search_item) | Q(slug__icontains=search_item)) & Q(status='p')),
                'submitbutton': submitbutton
            }
        return render(request, "shop/search.html", context)
    else:
        return render(request, "shop/search.html")

def faq(request):
    return render(request, 'shop/faq.html')


def about(request):
    return render(request, 'shop/about.html')
