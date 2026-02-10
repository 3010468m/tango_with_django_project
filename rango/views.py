from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from rango.forms import CategoryForm, PageForm
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

def add_category(request):
    form = CategoryForm()

    # a http post ?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # check provided form is valid
        if form.is_valid():
            # save new cat to database
            form.save(commit=True)
            # redirect to index view
            return redirect('/rango')
        else:
            # if form contains errors, print
            print(form.errors)

    # handles bad form, new form or no form cases
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST'
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


