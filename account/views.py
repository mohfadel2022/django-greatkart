from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verfication email
from django.contrib.sites.shortcuts import  get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name= first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone_number=phone_number,             
                password=password
            )
            user.save()

            # USER ACCOUNT ACTIVATION
            current_site = get_current_site(request)
            email_subject = 'Please activate you account'
            message = render_to_string('account/account_activation_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Thank You for registering. Verify your email to activate your account.')
            return redirect('/account/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'account/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Your are successful logged in.")
            return redirect('dashboard')
        else:            
            messages.error(request, "Invalid username o password")
            return redirect('login')

    return render(request, 'account/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation Your account now is actived.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')

    return redirect('register')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'account/dashboard.html')

def forgot_password(request):

    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email=email):
            user = Account.objects.get(email__exact=email)

            # PASSWORD RESET EMAIL
            current_site = get_current_site(request)
            email_subject = 'Reset Your password'
            message = render_to_string('account/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset email has been sent .")
            return redirect('login')
        else:            
            messages.error(request, "Account does not exists")
            return redirect('forgotPassword')   

    return render(request, 'account/forgot_password.html')

def reset_password_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        # user.password = ""
        # user.save()
        messages.success(request, 'Please reset Your password.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Invalid reset link.')
    
    return redirect('login')


def reset_password(request):

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            # PASSWORD RESET EMAIL
            current_site = get_current_site(request)
            email_subject = 'You been change Your password'
            message = render_to_string('account/new_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            send_email = EmailMessage(email_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset successful.")
            return redirect('login')
            # else:
            #     messages.error(request, "Un error occured!")
            #     return redirect('resetPassword') 
        else:            
            messages.error(request, "Passwords do not mutches !")
            return redirect('resetPassword')   
    else:
        return render(request, 'account/reset_password.html')