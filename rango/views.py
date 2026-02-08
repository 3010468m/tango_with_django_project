from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page

def index(request):
    # query database for list of all cats currently stored
    #order by likes in descending order
    # retrieve top 5 only
    # place list in context_dict
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    #render response and return
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html', {'title': 'About'})

def show_category(request, category_name_slug):
    # create context dict to pass to template rendering engine
    context_dict = {}

    try:
        #try find a cat name slug with given name
        # if cant, the .get() method raises exception
        # the .get() method returns one mode instance or raises exception
        category = Category.objects.get(slug=category_name_slug)

        # retrieve all associated pages
        pages = Page.objects.filter(category=category)

        #add results list to template context under name pages
        context_dict['pages'] = pages
        # also add cat obj from database to context dict
        context_dict['category'] = category
    except Category.DoesNotExist:
        # if no specified cat found, dont do anything
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)
