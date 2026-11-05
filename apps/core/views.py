from django.shortcuts import render

def inicio(request):
    return render(request, 'core/index.html')


def nosotros(request):
    return render(request, 'core/nosotros.html')