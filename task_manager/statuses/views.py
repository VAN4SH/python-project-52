from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.mixins import MyLoginRequiredMixin
from .models import Status
from .forms import StatusForm


class StatusListView(MyLoginRequiredMixin, ListView):
    template_name = "statuses/list.html"
    model = Status
    context_object_name = "statuses"
    extra_context = {"header": _("Statuses")}


class StatusCreateView(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "form.html"
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("statuses")
    success_message = _("Status is successfully created")
    extra_context = {
        "header": _("Create status"),
        "button_text": _("Create"),
    }


class StatusUpdateView(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "form.html"
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("statuses")
    success_message = _("Status is successfully changed")
    extra_context = {
        "header": _("Change status"),
        "button_text": _("Change"),
    }


class StatusDeleteView(MyLoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = Status
    success_url = reverse_lazy("statuses")
    success_message = _("Status is successfully deleted")
    protected_message = _("Unable to delete a status because it is in use")
    extra_context = {
        "header": _("Delete status"),
        "button_text": _("Yes, delete"),
    }

    def post(self, request, *args, **kwargs):
        if self.get_object().status.all().exists():
            messages.error(request, self.protected_message)
            return redirect(self.success_url)
        else:
            messages.success(request, self.success_message)
            return super().delete(request, *args, **kwargs)
