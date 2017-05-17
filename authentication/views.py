from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

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
