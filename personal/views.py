from django.shortcuts import render,redirect

# Create your views here.
def home_view(request):
    context = {}
    groups = ['hi','hello','hola']
    context['groups'] = groups
    if request.user.is_authenticated:
        return render(request,'personal/main.html',context)
    else:
        return redirect('login/')