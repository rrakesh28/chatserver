from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from account.models import Account
from django.http import HttpResponse
from account.forms import RegistrationForm,AccountAuthenticationForm,AccountUpdateForm
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import cv2
import json
import base64
import requests
from django.core import fiLes


TEMP_PROFILE_IMAGE_NAME = 'temp_profile_image.png'
# Create your views here.
def login_view(request,*args,**kwargs):
    context = {}

    if request.user.is_authenticated:
        return redirect('home')
    
    destination = get_redirect_if_exists(request)
    print('Destinaiton '+ str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request,'account/login.html',context)

def get_redirect_if_exists(request):
    redirect = None


def register_view(request,*args,**kwargs):

    if request.user.is_authenticated:
        return redirect('home')

    context ={}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            account = authenticate(email=email,password=raw_password)
            login(request,account)
            destination = kwargs.get('next')
            print("Destinaiton "+str(destination))
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request,'account/register.html',context)
    

def logout_view(request):
    logout(request)
    return redirect('home')


def account_view(request,*args,**kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    print(user_id)

    try:
        account = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse("The user doesn't exists")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        is_self = True
        is_friend = False
        user = request.user

        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request,'account/account.html', context)



def account_search_view(request,*args,**kwargs):
    context = {}

    if request.method == 'GET':
        search_query = request.GET['q']
        print("Search query ",search_query)

        if len(search_query) > 0:
            search_results = Account.objects.filter(username__icontains=search_query).distinct()
            accounts = []
            print("Search results ", search_results)
            for account in search_results:
                accounts.append((account,False))
                print("accounts ", account)
            context['accounts'] = accounts
    return render(request,'account/search_results.html',context)

def edit_account_view(request,*args,**kwargs):
    context = {}

    if not request.user.is_authenticated:
        return redirect('login')
    user_id = kwargs.get('user_id')

    try:
        account = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse('Something')
    if account.pk != request.user.pk:
        return HttpResponse("Something")
    
    if request.POST:
        form = AccountUpdateForm(request.POST,request.FILES, instance = request.user)
        if form.is_valid:
            #delete the old profile image
            # account.profile_image.delete()
            form.save()
            return redirect('account:view',user_id = account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance =request.user,
                initial = {
                    "id" : account.pk,
                    "email": account.email,
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
    else:
        form = AccountUpdateForm(
                initial = {
                    "id" : account.pk,
                    "email": account.email,
                    "username": account.username,
                    "profile_image": account.profile_image.url ,
                    "hide_email": account.hide_email,
                }
            )
        
        context['form'] = form
    
    context['DATA_UPLOAD_MAX_MEMROY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMROY_SIZE
    return render(request,'account/edit_account.html',context)

def save_temp_profile_image_form_base64String(imageString, user):
    INCRRECT_PADDING_EXCEPTION = "incorrect padding"

    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(f"{settings.TEMP}/{user.pk}"):
            os.mkdir(f"{settings.TEMP}/{user.pk}")
        url = os.paht.join(f"{settings.TEMP}/{user.pk}", TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)     
        image = base64.b64decode(imageString)
        with storage.open('','wb+') as destinaiton:
            destinaiton.write(image)
            destinaiton.close() 
        return url
    except Exception as e:
        if str(e) == INCRRECT_PADDING_EXCEPTION:
            imageSring += "=" * ((4 - len(imageSring) % 4) % 4)
            return save_temp_profile_image_form_base64String(imageSring, user)
    return None


def crop_image(request,*args,**kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageSring = request.POST.get('image')
            url = save_temp_profile_image_form_base64String(imageSting, user)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX'))))
            cropY = int(float(str(request.POST.get('cropY'))))
            cropWidht = int(float(str(request.POST.get('cropWidht'))))
            cropHeight = int(float(str(request.POST.get('cropHeight'))))

            if cropX < 0:
                cropX = 0

            if cropY < 0:
                cropY = 0

            crop_img = img[cropY: cropY + cropHeight, cropX: cropX+cropWidht]

            cv2.imwrite9url, crop_img

            user.profile_image.delete()

            user.profile_image.save('profile_image.png',files.File(open(url, 'rb')))
            user.save()

            payload['result'] : 'sucess'
            payload['cropped_profile_image'] = user.profile_image.url

            os.remove(url)

        except Exception as e:
            payload['result'] = 'error'
            payload['exception'] = str(e)

        return HttpResponse(json.dump(payload),context_type='application/json')