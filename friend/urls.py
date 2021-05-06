from django.urls import path
from friend.views import (
	send_friend_request,
	friend_requests,
	accept_friend_request,
	remove_friend,
)

app_name = 'friend'

urlpatterns = [
	path('friend_remove/',remove_friend, name='remove_friend'),
	path('friend_request/',send_friend_request,name='friend_request'),
	path('friend_request/<user_id>/',friend_requests,name='friend_request'),
	path('friend_request_accpt/<friend_request_id>/',accept_friend_request,name='friend_request_accept'),

]