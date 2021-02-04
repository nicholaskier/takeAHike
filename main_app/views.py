from django.shortcuts import render
from .models import Hike
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def home(request):
    return render(request, 'home.html')

def hikes_index(request):
    hikes = Hike.objects.all()
    return render(request, 'hikes/index.html', {'hikes': hikes})

def hikes_detail(request, hike_id):
    hike = Hike.objects.get(id=hike_id)
    return render(request, 'hikes/detail.html', {'hike': hike})
# Create your views here.

class HikeCreate(CreateView):
    model = Hike
    fields = ['title', 'summary', 'distance']

class HikeUpdate(UpdateView):
    model = Hike
    fields = ['title', 'summary', 'distance']

class HikeDelete(DeleteView):
    model = Hike
    success_url = '/hikes/'
