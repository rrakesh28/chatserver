from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
import json

def room(request, *args, **kwargs):
	context = {}

	if request.user.is_authenticated:

		context['room_name'] = kwargs.get('room_name')
		context['username'] = (request.user.username)
		print(context['room_name'])
		return render(request,'chat/room.html',context)
	else:
		return redirect('login')
