from django.urls import path
from friend.views import (
	send_friend_request,
	friend_requests,
	accept_friend_request,
	remove_friend,
	decline_friend_request,
	cancel_friend_request,
	friend_list_view,
)

app_name = 'friend'

urlpatterns = [
	path('list/<user_id>/',friend_list_view,name='list'),
	path('friend_remove/',remove_friend, name='remove_friend'),
	path('friend_request/',send_friend_request,name='friend_request'),
	path('friend_request/<user_id>/',friend_requests,name='friend_request'),
	path('friend_request_accept/<friend_request_id>/',accept_friend_request,name='friend_request_accept'),	
	path('friend_request_decline/<friend_request_id>/',decline_friend_request,name='friend_request_decline'),	
	path('friend_request_cancel/',cancel_friend_request,name='friend_request_cancel'),
]