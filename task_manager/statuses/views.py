from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.mixins import MyLoginRequiredMixin
from .models import Status
from .forms import StatusForm
from task_manager.tasks.models import Task
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


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


class StatusDeleteView(MyLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Статус успешно удалён')
    extra_context = {
        'header': _('Удаление статуса'),
        'button_text': _('Да, удалить'),
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                _('Unable to delete a status because it is in use'))
            return redirect('statuses')

