from django.shortcuts import render, redirect
from post.models import Post

# Create your views here.

def post_page_view(request, *args, **kwargs):
	context = {}
	if request.user.is_authenticated:
		return render(request,'post/add_post_page.html',context)
	else:
		return redirect('login')


def add_post(request, *args, **kwargs):
	
	context = {}
	user = request.user

	if user.is_authenticated: 
		if request.method == "POST":
			content = request.POST['post_data']
			post = Post(creator=user, content=content)
			post.save()
			return redirect('home')
	else:
		return redirect('login')





