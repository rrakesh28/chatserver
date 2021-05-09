from django.shortcuts import render, redirect

from django.http import HttpResponse
import json
from account.models import Account
from friend.models import FriendRequest, FriendList


def friend_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get('user_id')

		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Exception as e:
				return HttpResponse("That user doesnot Exist")

			try:
					friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse("Couldn't find a friend")

			#must be friends to view a friends list
			if user != this_user:
				if not user in friend_list.friends.all():
					return HttpResponse("You need to be friends")
			

			friends = []
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))

			context['friends'] = friends
	else:
		return HttpResponse("You be ")
	return render(request,'friend/friend_list.html',context)

def friend_requests(request, *args, **kwargs):
	context = {}

	user = request.user

	if user.is_authenticated:
		user_id = kwargs.get('user_id')
		account = Account.objects.get(pk=user_id)
		if account == user:
			friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
			context['friend_requests'] = friend_requests
		else:
			return HttpResponse(" You can't view another users friend requests")
	else:
		redirect("login")
	return render(request, 'friend/friend_requests.html',context)

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

def accept_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now accept it
					updated_notification = friend_request.accept()
					payload['response'] = "Friend request accepted."

				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your request to accept."
		else:
			payload['response'] = "Unable to accept that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to accept a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def remove_friend(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = Account.objects.get(pk=user_id)
				friend_list = FriendList.objects.get(user=user)
				friend_list.unfriend(removee)
				payload['response'] = "Successfully removed that friend."
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove that friend."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to remove a friend."
	return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now decline it
					friend_request.decline()
					payload['response'] = "Friend request declined."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your friend request to decline."
		else:
			payload['response'] = "Unable to decline that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to decline a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def cancel_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}

	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get('receiver_user_id')
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
			except Exception as e:
				payload['response'] = 'Nothing is cancel. Friend request does not exist.'

			#there should only be a single active friend request at any given time.
			#Cancel them all just in case.

			if len(friend_requests) > 1:
				for request in friend_requests:
					request.cancel()
				payload['response'] = 'Friend request cancelled.'
			else:
				friend_requests.first().cancel()
				payload['response'] = 'Friend Request cancelled.'
		else:
			payload['response'] = 'Unable to cancel that friend request.'
	else:
		paylod['response'] = 'You must be authenticated to cancel the request'

	return HttpResponse(json.dumps(payload),content_type="application/json")