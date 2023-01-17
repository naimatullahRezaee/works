from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "main.html")

def error_404_view(request, exception):
   
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')