from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator', default=None)
	content = models.TextField(blank=False)

	def __str__(self):
		return self.creator.username

	def add_post(self, post):
		self.post.add(post)
		self.save()

	def remove_post(self, post):
		self.post.remove(post)
		self.save()