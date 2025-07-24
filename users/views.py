from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.conf import settings
from django.shortcuts import redirect

from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = settings.DEFAULT_FROM_EMAIL  # твой email из settings.py
        recipient_list = [user_email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm


def simple_logout(request):
    logout(request)
    return redirect('login')

