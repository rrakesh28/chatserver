from django.shortcuts import render

from django.http import HttpResponse
import json
from account.models import Account
from friend.models import FriendRequest

def send_friend_request(request,*args, **kwargs):
	user = request.user

	payload = {}

	if request.method == 'POST' and user.is_authenticated:
		user_id = request.POST.get('receiver_user_id')
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				#Get all friend requests active and in active
				friend_requests = FriendRequest.objects.filter(sender=user,receiver=receiver)
				try:
					#check whether the request is active
					for request in friend_requests:
						if request.is_active:
							raise Exception("You already sent a friend request.")
					#if the request is not active and not in the list then save the request
					friend_request = FriendRequest(sender=user,receiver=receiver)
					friend_request.save()
					payload['response'] = 'Friend Request Sent.'

				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				friend_request = FriendRequest(sender=user,receiver=receiver)
				friend_request.save()
				payload['response'] = 'Friend Request Sent.'

			if payload['response'] == None:
				payload['response'] = 'Something went wrong'
		else:
			payload['response'] = 'Unable send a friend request'
	else:
		payload['response'] = 'You must be authenticated to send a friend request'

	return HttpResponse(json.dumps(payload),content_type='application/json')
			