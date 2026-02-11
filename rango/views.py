from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
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
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})

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

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
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


def register(request):
    # was registration successful
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #hash password
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            # check for pfp
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # not a http post
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html',context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check username/password is valid
        user = authenticate(username=username, password=password)

        if user:
            # check account is active
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            # bad login details provided
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # we know user is logged in, so can just log them out
    logout(request)
    return redirect(reverse('rango:index'))