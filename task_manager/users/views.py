from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.tasks.models import Task
from task_manager.mixins import (
    MyLoginRequiredMixin,
    SelfCheckUserMixin,
)
from .models import MyUser
from .forms import UserCreateForm, UserUpdateForm


class UserListView(ListView):
    model = MyUser
    template_name = "users/list.html"
    context_object_name = "users"
    extra_context = {
        "header": _("Users"),
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = MyUser
    form_class = UserCreateForm
    template_name = "form.html"
    success_url = reverse_lazy("login")
    success_message = _("User is created successfully")
    extra_context = {
        "header": _("Registration"),
        "button_text": _("Register "),
    }


class UserUpdateView(
    MyLoginRequiredMixin, SelfCheckUserMixin, SuccessMessageMixin, UpdateView
):
    template_name = "form.html"
    model = MyUser
    form_class = UserUpdateForm
    success_url = reverse_lazy("users")
    success_message = _("User is successfully updated")
    permission_message = _("You have no rights to change another user.")
    permission_url = reverse_lazy("users")
    extra_context = {
        "header": _("Update user"),
        "button_text": _("Update"),
    }


class UserDeleteView(
    MyLoginRequiredMixin,
    SelfCheckUserMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "delete.html"
    model = MyUser
    success_url = reverse_lazy("users")
    success_message = _("User is successfully deleted")
    permission_message = _("You have no rights to change another user.")
    permission_url = reverse_lazy("users")
    extra_context = {
        "header": _("Deleting user"),
        "button_text": _("Yes, delete"),
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (
            Task.objects.filter(author=self.object).exists()
            or Task.objects.filter(executor=self.object).exists()
        ):
            messages.error(request, _("Unable to delete a user because they are in use"))
            return redirect(reverse_lazy("users"))
        else:
            return super().delete(request, *args, **kwargs)
