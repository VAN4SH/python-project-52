from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import (
    MyLoginRequiredMixin,
    SelfCheckUserMixin,
    CanDeleteProtectedEntityMixin,
)
from .models import MyUser
from .forms import UserCreateForm, UserUpdateForm


class HeaderButtonMixin:
    header = ""
    button_text = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.header:
            context["header"] = self.header
        if self.button_text:
            context["button_text"] = self.button_text
        return context


class UserListView(HeaderButtonMixin, ListView):
    model = MyUser
    template_name = "users/list.html"
    context_object_name = "users"
    header = _("Users")


class UserCreateView(HeaderButtonMixin, SuccessMessageMixin, CreateView):
    model = MyUser
    form_class = UserCreateForm
    template_name = "form.html"
    success_url = reverse_lazy("login")
    success_message = _("User is created successfully")
    header = _("Registration")
    button_text = _("Register")


class UserUpdateView(
    HeaderButtonMixin,
    MyLoginRequiredMixin,
    SelfCheckUserMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = MyUser
    form_class = UserUpdateForm
    template_name = "form.html"
    success_url = reverse_lazy("users")
    success_message = _("User is successfully updated")
    permission_message = _("You have no rights to change another user.")
    permission_url = reverse_lazy("users")
    header = _("Update user")
    button_text = _("Update")


class UserDeleteView(
    HeaderButtonMixin,
    MyLoginRequiredMixin,
    SelfCheckUserMixin,
    CanDeleteProtectedEntityMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = MyUser
    template_name = "delete.html"
    success_url = reverse_lazy("users")
    success_message = _("User is successfully deleted")
    permission_message = _("You have no rights to change another user.")
    permission_url = reverse_lazy("users")
    protected_message = _("Unable to delete a user because they are in use")
    protected_url = reverse_lazy("users")
    header = _("Deleting user")
    button_text = _("Yes, delete")
