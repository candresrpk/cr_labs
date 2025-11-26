from django.shortcuts import render

# Create your views here.


def webHomeView(request):
    context = {
        'title': 'C&R - Home',
    }
    return render(request, 'web/index.html', context)