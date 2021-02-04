from django.shortcuts import render, redirect
from .models import Hike, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3

session = boto3.Session(profile_name='hikes')
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'takeahike'


def home(request):
    return render(request, 'home.html')

def hikes_index(request):
    hikes = Hike.objects.all()
    return render(request, 'hikes/index.html', {'hikes': hikes})

def hikes_detail(request, hike_id):
    hike = Hike.objects.get(id=hike_id)
    return render(request, 'hikes/detail.html', {'hike': hike})
# Create your views here.
def add_photo(request, hike_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # console.log(url)
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, hike_id=hike_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', hike_id=hike_id)

class HikeCreate(CreateView):
    model = Hike
    fields = ['title', 'summary', 'distance']

class HikeUpdate(UpdateView):
    model = Hike
    fields = ['title', 'summary', 'distance']

class HikeDelete(DeleteView):
    model = Hike
    success_url = '/hikes/'
