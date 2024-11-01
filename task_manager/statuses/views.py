from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.mixins import MyLoginRequiredMixin
from .models import Status
from .forms import StatusForm
from task_manager.tasks.models import Task


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
    extra_context = {
        "header": _("Delete status"),
        "button_text": _("Yes, delete"),
    }

    def form_valid(self, form):
        messages.success(request=self.request, message=self.success_message)
        return super(StatusDeleteView, self).form_valid(form)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(
                request, _("Unable to delete the status because it is in use.")
            )
            return redirect(self.success_url)
        else:
            messages.success(request, self.success_message)
            return super().delete(request, *args, **kwargs)
