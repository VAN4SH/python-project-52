from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "form.html"
    form_class = AuthenticationForm
    extra_context = {
        "header": _("Login"),
        "button_text": _("Enter"),
    }
    success_message = _("You are logged in")


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
