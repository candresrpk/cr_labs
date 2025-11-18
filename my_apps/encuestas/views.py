from django.shortcuts import render

# Create your views here.


def home(request):
    context = {
        'title': 'Hossaik',
    }
    return render(request, 'encuestas/index.html', context)