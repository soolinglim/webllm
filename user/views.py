from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

from registration import signals
from registration.backends.simple.views import RegistrationView
from django.utils.safestring import mark_safe

User = get_user_model()

def anonymous_required(function=None, redirect_url=None): # decorator taken from http://djangosnippets.org/snippets/2969/ 
    if not redirect_url:
        redirect_url = 'person_landing'

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url,
        # redirect_field_name=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


class CustomRegistrationView(RegistrationView):
    success_url = 'person_landing'
    template_name = 'registration/registration_form.html'


class UserProfile(UpdateView):
    model = User
    fields = ['email',]
    template_name = 'registration/profile.html'

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.user.id)
        return obj

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile updated.')
        return reverse('user_profile')

