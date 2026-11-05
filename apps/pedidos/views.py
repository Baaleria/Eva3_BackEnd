from django.shortcuts import render


def ver(request):
    return render(request, 'pedidos/ver.html')
