from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import UserCreation
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.utils.crypto import get_random_string
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    template="main/index.html"
    return render(request, template)

def event(request):
    template="main/event.html"
    return render(request, template)

def event_details(request):
    template="main/event_details.html"
    return render(request, template)





def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return render(request, 'signup.html', {'error_message': "Your password and confirm password do not match."})
        else:
            try:
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.is_active = False  # Set the user as inactive until approved by admin
                my_user.save()
            except IntegrityError:
                return render(request, 'signup.html', {'error_message': "Username or email already exists."})

            # Generate a unique token for account approval
            token = get_random_string(length=32)

            # Create a UserCreation object
            user_creation = UserCreation.objects.create(user=my_user, token=token)

            # Step 3: Send email notification to the admin
            subject = 'New account creation request'
            message = f"Username: {uname}\nEmail: {email}\nPlease approve or delete this account creation request.\n\n"
            message += f"Click here to approve: {request.build_absolute_uri(reverse('approve_user_creation', kwargs={'token': token}))}"
            from_email = 'access.users0@gmail.com'
            to_email = 'access.users0@gmail.com'
            send_mail(subject, message, from_email, [to_email])

            return render(request, 'signup_confirmation.html')

    return render(request, 'signup.html')

def LoginPage(request):
    error_message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index') 
            elif user.groups.filter(name='researchers').exists():
                return redirect('researcher:index') 
            else:
                return redirect('index') 
        else:
            error_message = "Username or Password is incorrect!!!"

    context = {
        'error_message': error_message
    }
    return render(request, 'login.html', context)


@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('index')

@staff_member_required
def LogoutPage(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def AdminPage(request):
    if not request.user.is_superuser:
        return redirect('login')

    # Step 4: Retrieve pending account creation requests
    user_creations = UserCreation.objects.filter(approved=False)

    context = {'user_creations': user_creations}
    return render(request, 'admin.html', context)


@staff_member_required(login_url='admin:login')
def approve_user_creation(request, token):
    try:
        user_creation = get_object_or_404(UserCreation, token=token)
    except UserCreation.DoesNotExist:
        messages.error(request, "User creation request does not exist.")
        return redirect('admin:index')

    if request.method == 'POST':
        if 'approve' in request.POST:
            # Activate the user's account
            my_user = user_creation.user
            my_user.is_active = True
            my_user.is_staff = True
            my_user.save()

            # Assign the group to the user
            researchers, _ = Group.objects.get_or_create(name='researchers')
            my_user.groups.add(researchers)

            # Step 6: Send email notification to the user
            subject = 'Account creation approved'
            message = 'Your account creation request has been approved.\n\n'
            message += f"Click here to login: {request.build_absolute_uri(reverse('login'))}"
            from_email = 'access.users0@gmail.com'
            to_email = user_creation.user.email
            send_mail(subject, message, from_email, [to_email])

        elif 'disapprove' in request.POST:
            # Step 7: Send email notification to the user
            subject = 'Account creation disapproved'
            message = 'Your account creation request has been disapproved.\n\n'
            from_email = 'access.users0@gmail.com'
            to_email = user_creation.user.email
            send_mail(subject, message, from_email, [to_email])

            # Delete the user creation request and the associated user
            user_creation.user.delete()
            user_creation.delete()

        return redirect('admin:index')

    admin_url = reverse('admin:index')
    context = {'user_creation': user_creation, 'admin_url': admin_url}
    return render(request, 'approve.html', context)

@login_required(login_url='login')
def delete_user_creation(request, user_creation_id):
    if not request.user.is_superuser:
        return redirect('login')

    user_creation = UserCreation.objects.get(id=user_creation_id)

    # Retrieve the user associated with the user creation request
    user = user_creation.user

    # Delete the user creation request and the associated user
    user_creation.delete()
    user.delete()

    return redirect('admin')


def SignupConfirmationPage(request):
    return render(request, 'signup_confirmation.html')