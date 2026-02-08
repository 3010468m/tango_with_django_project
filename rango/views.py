from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category

def index(request):
    # query database for list of all cats currently stored
    #order by likes in descending order
    # retrieve top 5 only
    # place list in context_dict
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    #render response and return
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html', {'title': 'About'})