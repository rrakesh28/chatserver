from enum import Enum

class  FriendRequestStatus(Enum):
	"""docstring for  FriendReuestStatus"""
	NO_REQUEST_SENT = 0
	THEY_SENT_TO_YOU = 1
	YOU_SENT_TO_THEM = -1
