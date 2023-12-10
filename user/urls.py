from django.urls import include, re_path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .views import anonymous_required, CustomRegistrationView, UserProfile
from .forms import UserCreationForm


urlpatterns = [
    re_path(r'^login/$',
        anonymous_required(auth_views.LoginView.as_view(
            template_name='registration/login.html')),
        name='auth_login'),
    re_path(r'^logout/$',
        auth_views.LogoutView.as_view(
            template_name='registration/logout.html'),
        name='auth_logout'),
    re_path(r'^password/change/$',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy('auth_password_change_done')),
        name='password_change'),
    re_path(r'^password/change/done/$',
        auth_views.PasswordChangeDoneView.as_view(),
        name='auth_password_change_done'),
    re_path(r'^password/reset/$',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('password_reset_done')),
        name='password_reset'),
    re_path(r'^password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    re_path(r'^password/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('password_reset_complete')),
        name='password_reset_confirm'),
    re_path(r'^signup/$', anonymous_required(CustomRegistrationView.as_view(form_class=UserCreationForm)), name='registration_register'),
    # re_path(r'^profile/$', login_required(UserProfile.as_view()), name='user_profile'),
]
