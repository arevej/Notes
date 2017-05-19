from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Note

import json

def index (request):
    if request.user.is_authenticated():
        all_notes = request.user.note_set.all()
        context = {'all_notes': all_notes}
        return render(request, 'notes/notes.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def register (request):
    if request.method == 'GET':
        return render(request, 'registration/register.html', {})
    else:
        login_ = request.POST['login']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.create_user(login_, email, password)
            user=authenticate(request, username=login_, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('notes'))
        except Exception as e:
            return render(request, 'registration/register.html', { 'error': str(e) })

@csrf_exempt
def update_note (request, note_id):
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        json_data = json.loads(request.body)
        note.coord_x = json_data['coord_x']
        note.coord_y = json_data['coord_y']
        note.height = json_data['height']
        note.width = json_data['width']
        note.color = json_data['color']
        note.text = json_data['text']
        note.save()
        return HttpResponse('')
    elif request.method == 'DELETE':
        note.delete()
        return HttpResponse('')

@csrf_exempt
def create_note (request):
    note = Note()
    note.user = request.user
    json_data = json.loads(request.body)
    note.coord_x = json_data['coord_x']
    note.coord_y = json_data['coord_y']
    note.height = json_data['height']
    note.width = json_data['width']
    note.color = json_data['color']
    note.text = json_data['text']
    note.save()
    return HttpResponse(str(note.id))
