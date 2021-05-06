from django.shortcuts import render,redirect
from post.models import Post

# Create your views here.
def home_view(request):
    context = {}
    posts = []
    user = request.user

    if user.is_authenticated:
    	users_post = Post.objects.all()

    	for post in reversed(users_post):
    		posts.append(post)

    	if users_post:
    		context['posts'] = posts
    	return render(request,'personal/main.html',context)
    else:
    	return redirect('login/')