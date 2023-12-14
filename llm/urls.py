from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views import *

urlpatterns = [
    re_path(r'^history/(?P<uuid_param>[0-9a-fA-F-]+)/$', get_history, name="llm_history"),
    re_path(r'^history/$', get_all_runs, name="llm_all_runs"),
    re_path(r'^$', TemplateView.as_view(template_name="llm/landing.html"), name='llm_landing'),
    path('ajax_process_user_input/', ajax_process_user_input, name='ajax_process_user_input'),
    path('ajax_get_image/', ajax_get_image, name='ajax_get_image'),
    path('ajax_crossover/', ajax_crossover, name='ajax_crossover'),
    # path('ajax_mail_admin/', ajax_mail_admin, name='ajax_mail_admin'),
    path('ajax_run_complete/', ajax_run_complete, name='ajax_run_complete'),
    path('ajax_favourite_image/', ajax_favourite_image, name='ajax_favourite_image'),
    path('ajax_final_feedback/', ajax_final_feedback, name='ajax_final_feedback'),
]
