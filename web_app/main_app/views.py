from django.shortcuts import render


def index(request):
    return render(request, 'main_app/main_app_start.html')


def about(request):
    return render(request, 'main_app/main_app_about.html')
