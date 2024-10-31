from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class MyLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not logged in! Please log in."))
            return redirect(reverse_lazy("login"))

        return super().dispatch(request, *args, **kwargs)


class SelfCheckUserMixin(UserPassesTestMixin):
    permission_message = None
    permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class CanDeleteProtectedEntityMixin:
    protected_message = None
    protected_url = None

    def has_related_objects(self, obj):
        for rel in obj._meta.get_fields():
            if rel.one_to_many or rel.one_to_one:
                accessor_name = rel.get_accessor_name()
                related_queryset = getattr(obj, accessor_name)
                if related_queryset.exists():
                    return True
            elif rel.many_to_many:
                related_manager = getattr(obj, rel.name)
                if related_manager.exists():
                    return True
        return False

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.has_related_objects(obj):
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
        else:
            return super().post(request, *args, **kwargs)


class AuthorCanDeleteTaskMixin(UserPassesTestMixin):
    author_check_message = None
    author_check_url = None

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.author_check_message)
        return redirect(self.author_check_url)
