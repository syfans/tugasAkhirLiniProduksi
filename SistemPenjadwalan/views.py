from django.shortcuts import render, redirect


def index(request):
    context = {
        'Judul': 'Home',
    }
    template_name = None

    if request.user.is_authenticated:
        #logika untuk user
        template_name ='mainPage.html'
    else:
        #logika untuk anonymous user
        template_name ='index_anonymous_base.html'
    return render(request,template_name,context)

def home(request):
    context = {
        'Judul': 'Home',
    }
    return render(request, 'home.html', context)

def contributor(request):
    context = {
        'Judul': 'Contributor',
    }
    return render(request, 'contributor.html', context)