from django.shortcuts import render, redirect, get_object_or_404
from .models import Hike, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import uuid
import boto3

# session = boto3.Session(profile_name='hikes')
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'takeahike'


def home(request):
    return render(request, 'home.html')

@login_required
def hikes_index(request):
    hikes = Hike.objects.filter(user=request.user)
    return render(request, 'hikes/index.html', {'hikes': hikes})

@login_required
def hikes_detail(request, hike_id):
    hike = Hike.objects.get(id=hike_id)
    total_likes = hike.total_likes()
    return render(request, 'hikes/detail.html', {'total_likes': total_likes, 'hike': hike})
# Create your views here.
@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)    

def LikeView(request, pk):
    hike = get_object_or_404(Hike, id=request.POST.get('hike_id'))
    hike.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))

class HikeCreate(LoginRequiredMixin, CreateView):
    model = Hike
    fields = ['title', 'summary', 'distance']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HikeUpdate(LoginRequiredMixin, UpdateView):
    model = Hike
    fields = ['title', 'summary', 'distance']

class HikeDelete(LoginRequiredMixin, DeleteView):
    model = Hike
    success_url = '/hikes/'
