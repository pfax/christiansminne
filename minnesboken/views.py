from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse, redirect
from .models import Memory, Picture, Writing    # CloudinaryPhoto
from random import randint
from django.utils import timezone
from .forms import MemoryForm, MemoryTimelineForm    # PictureForm,
# import datetime
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
# from django import forms


cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    api_key=os.environ.get('CLOUDINARY_API_KEY', ''),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', '')
)


def new_timeline_post(request):
    if request.user.is_authenticated and request.user.is_activated:
        if request.method == "POST":
            form = MemoryTimelineForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.userprofile = request.user
                post.pub_date = timezone.now()
                post.text = request.text
                post.is_on_timeline = True
                post.timeline_date = request.timeline_date
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = MemoryTimelineForm()
        return render(request, 'minnesboken/memories/memory_edit.html', {'form': form})


def new_post(request):
    if request.user.is_authenticated and request.user.is_activated:
        if request.method == "POST":
            form = MemoryForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.userprofile = request.user
                post.pub_date = timezone.now()
                post.text = request.text
                post.is_on_timeline = True
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = MemoryForm()
        return render(request, 'minnesboken/memories/memory_edit.html', {'form': form})


def landingpage(request):
    public_writings = Writing.objects.filter(is_featured_publicly=True)
    public_pictures = Picture.objects.filter(is_featured_publicly=True)
    public_memories = Memory.objects.filter(is_featured_publicly=True)

    if public_writings.count() > 0:
        random_writing = public_writings[randint(0, public_writings.count() - 1)]
    else:
        random_writing = "No public writings."

    if public_pictures.count() > 0:
        random_picture = public_pictures[randint(0, public_pictures.count() - 1)]
    else:
        random_picture = "No public pictures."

    if public_memories.count() > 0:
        random_memory = public_memories[randint(0, public_memories.count() - 1)]
    else:
        random_memory = "No public memories."

    return render(request, 'minnesboken/landingpage.html', {
                           'random_picture': random_picture,
                           'random_memory': random_memory,
                           'random_writing': random_writing})


def timeline(request):
    timeline_memories_list = Memory.objects.filter(is_on_timeline=True).order_by('timeline_date')
    return render(request, 'minnesboken/memories/timeline.html', {'timeline_memories_list': timeline_memories_list, })


def memories(request):
    latest_memories_list = Memory.objects.filter(is_on_timeline=False).order_by('-pub_date')[:5]
    # latest_memories_list = Memory.objects.order_by
    # pics = get_list_or_404(UserProfile)
    context = {'latest_memories_list': latest_memories_list}
    return render(request, 'minnesboken/memories/memories.html', context)


def memory_detail(request, memory_id):
    memory = get_object_or_404(Memory, pk=memory_id)
    return render(request, 'minnesboken/memories/memory_detail.html', {'memory': memory})


def pictures(request):
    latest_pictures_list = Picture.objects.order_by('-date_taken')[:5]
    context = {'latest_pictures_list': latest_pictures_list}
    return render(request, 'minnesboken/pictures/pictures.html', context)


def picture_detail(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    return render(request, 'minnesboken/pictures/picture_detail.html', {'picture': picture})


def writings(request):
    writings_list = Writing.objects.all()
    return render(request, 'minnesboken/writings/writings.html', {'writings_list': writings_list})


def writing_detail(request, writing_id):
    writing = get_object_or_404(Writing, pk=writing_id)
    return render(request, 'minnesboken/writings/writing_detail.html', {'writing': writing})


def post_memory(request):  # TODO: Have some fun here
    if request.user.is_authenticated() is False:
        return HttpResponseForbidden()
    else:

        mymemory = Memory(userprofile=request.user, memory_text=request.POST['text'], pub_date=timezone.now())
        mymemory.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('memories'))
