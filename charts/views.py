from django.shortcuts import render
from . import plotly_app
from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, 'index.html')