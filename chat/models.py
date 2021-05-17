from django.db import models
from django.conf import settings

class Message(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_messages',on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.username

	def last_10_messages():
		return Message.objects.all()



