from django.shortcuts import render, redirect
from django.http import HttpResponse
import qrcode
from .models import UserData, Register
from django.contrib.auth import authenticate,login,logout
from .models import UserData
import re
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.template import loader
import base64





def login_page(request):
    if request.method == "GET":
        return render(request, 'loginpage.html')
    else:
        user_id = request.POST.get('userid').lower()
        password = request.POST.get('password')
        user = authenticate(username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('userdata')
        else:
            messages.error(request, 'Invalid login credentials. Please try again')
            return redirect('login_page')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        fname = request.POST.get('fullname')
        user_id = request.POST.get('userid').lower()
        email = request.POST.get('emailid')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-=_+<>?]).{8,}$')

        # Check if user_id already exists
        if User.objects.filter(username=user_id).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'register.html')

        # Check passwords and pattern
        if password1 == password2 and password_pattern.match(password1):
            my_user = User.objects.create_user(username=user_id, email=email, password=password1)
            my_user.save()
            Register(
                Name=fname,
                User_ID=user_id,
                Email=email,
                Mobile=mobile,
                Address=address,
                Password1=password1,
                Password2=password2,
            ).save()
            messages.success(request, 'Registration successful. Please login here!')
            return redirect('login_page')
        else:
            if password1 != password2:
                messages.error(request, ' * Password and confirm password must be the same.')
            if not password_pattern.match(password1):
                messages.error(request, ' * Password must contain lowercase, uppercase, special character, and digits.')
            return render(request, 'register.html')



@login_required(login_url="login_page")
def userdata(request):
    context = {}
    if request.method == "POST":
        qr_text = request.POST.get("input", "")
        qr_image = qrcode.make(qr_text, box_size=10)
        qr_image_pil = qr_image.get_image()
        stream = BytesIO()
        qr_image_pil.save(stream, format='JPEG')
        qr_image_data = stream.getvalue()
        qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
        context['qr_image_base64'] = qr_image_base64
        context['variable'] = qr_text
        # Add a URL for downloading the QR code
        context['download_url'] = f"/download_qr/{qr_text}/"  # Adjust as per your URL configuration


    return render(request, 'userdata.html', context=context)

    


def download_qr_code(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data', '')
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        response.write(base64.b64decode(qr_data))
        return response
    else:
        return HttpResponse("Invalid request for QR code download.")



def user_logout(request):
    logout(request)
    return render(request,'loginpage.html')

    