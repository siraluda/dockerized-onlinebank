from django.shortcuts import render, reverse, redirect
from .forms import UserSignUp, CustomerProfileForm, CustomLoginForm
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate

class CustomerProfileUpdate(View):

    def get(self, request):
        customer_profile_form = CustomerProfileForm(
            instance=request.user.customerprofile)
        user_signup_form = UserSignUp(instance=request.user)

        context = {
            'c_form': customer_profile_form,
            'u_form': user_signup_form,
        }

        return render(request, 'users/profile.html', context)

    def post(self, request):
        c_form = CustomerProfileForm(
            request.POST, instance=request.user.customerprofile)
        u_form = UserSignUp(request.POST, instance=request.user)
        c_form.instance.customer = request.user
        customer_id = request.user.id

        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            return redirect(reverse('users:login'))


class CustomLoginView(View):

    def get(self, request):
        form = CustomLoginForm()

        return render(request, 'users/login.html', {'form':form})

    def post(self, request):
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')  

            try:
                # authenticate user          
                user = authenticate(email=email, password=password)
                user_id = user.id
            
            except AttributeError:
                return render(request, 'users/login.html', {'form': form, 'error_message': 'Invalid email or password'})

            else:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('accounts:customer-account-page', args=(user_id,)))
            
        return render(request, 'users/login.html', {'form': form})

class SignupView(View):

    def get(self, request):
        form = UserSignUp()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = UserSignUp(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('users:login'))
        return render(request, 'users/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('users:home'))

def index(request):
    return render(request, 'users/index.html')
