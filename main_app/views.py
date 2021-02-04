from django.shortcuts import render
from .models import Hike


def home(request):
    return render(request, 'home.html')

def hikes_index(request):
    hikes = Hike.objects.all()
    return render(request, 'hikes/index.html', {'hikes': hikes})

# Create your views here.
