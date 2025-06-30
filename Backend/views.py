import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *

from Backend.decorateur import permission_requise
from Backend.formulaire import *
from Backend.models import *

User = get_user_model()


@login_required
def home(request):
    user = request.user
    a = Association.objects.filter(pk=1)
    b = Association.objects.first()
    nbreM = Membre.objects.count()
    nbreUser = Utilisateur.objects.count()
    template = "accueil.html"
    return render(request, template,
                  context={"user": user, "asso": a, "nbreMembre": nbreM, "nbreUser": nbreUser, "a": b})


@method_decorator(permission_requise("creer membre"), name='dispatch')
class CreateMembre(CreateView):
    model = Membre
    form_class = MembreForm
    template_name = "admin/CreationMembre.html"
    success_url = reverse_lazy("Backend:createMembre")

    def form_valid(self, form):
        messages.success(self.request, "Le membre a été créée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()
        context["a"] = a
        return context


@method_decorator(permission_requise("creer membre"), name='dispatch')
class CreateRoleMembre(CreateView):
    model = RoleMembre
    form_class = MembreForm
    template_name = "admin/CreationMembre.html"
    success_url = reverse_lazy("Backend:createMembre")

    def form_valid(self, form):
        messages.success(self.request, "Le membre a été créée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()
        context["a"] = a
        return context


class CustomLoginView(LoginView):
    template_name = "registration/login.html"  # ou ton template spécifique

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["a"] = Association.objects.first()  # ou .get(pk=1), etc.
        return context


@method_decorator(permission_requise("modification association"), name='dispatch')
class ParamettrageAssociation(UpdateView):
    template_name = "admin/modificationAssociation.html"
    model = Association
    form_class = AssociationForm
    context_object_name = "association"
    success_url = reverse_lazy("Backend:home")

    def form_valid(self, form):
        messages.success(self.request, "Modification effectuée avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()
        context["a"] = a
        return context


@method_decorator(permission_requise("ajouter role utilisateur"), name='dispatch')
class CreationRoleUser(CreateView):
    model = RoleUser
    form_class = RoleUserForm
    template_name = "admin/role/creation.html"
    success_url = reverse_lazy("Backend:CreationRoleUser")

    def form_valid(self, form):
        messages.success(self.request, "Creation effectuée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()
        role_user = RoleUser.objects.all()
        context["a"] = a
        context['role'] = role_user
        return context


@method_decorator(permission_requise("ajouter role utilisateur"), name='dispatch')
class Supprimer_role(DeleteView):
    model = RoleUser
    template_name = 'admin/role/Creation.html'
    success_url = reverse_lazy('Backend:CreationRoleUser')

    def form_valid(self, form):
        messages.success(self.request, "suppression effectuée avec succès !")
        return super().form_valid(form)


@method_decorator(permission_requise("modifier role utilisateur"), name='dispatch')
class ModifierRoleUser(UpdateView):
    template_name = "admin/role/form_partial.html"
    model = RoleUser
    form_class = RoleUserForm
    context_object_name = "donne"
    success_url = reverse_lazy("Backend:CreationRoleUser")

    def form_valid(self, form):
        messages.success(self.request, "Modification effectuée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()

        context["a"] = a

        return context


@method_decorator(permission_requise("ajouter utilisateur"), name='dispatch')
class AjouterUtilisateur(CreateView):
    model = Utilisateur
    form_class = UtilisateurForm
    template_name = 'admin/users/ajoutUtilisateur.html'
    success_url = reverse_lazy('Backend:AjouterUtilisateur')

    def form_valid(self, form):
        messages.success(self.request, "Utilisateur ajouter  avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()
        utilisateur = Utilisateur.objects.all()

        context["a"] = a
        context["utilisateurs"]= utilisateur

        return context

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)


@method_decorator(permission_requise("ajouter utilisateur"), name='dispatch')
class Supprimer_user(DeleteView):
    model = Utilisateur
    template_name = 'admin/users/ajoutUtilisateur.html'
    success_url = reverse_lazy('Backend:AjouterUtilisateur')

    def form_valid(self, form):
        messages.success(self.request, "suppression effectuée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)


@method_decorator(permission_requise("modifier utilisateur"), name='dispatch')
class ModifierUser(UpdateView):
    template_name = "admin/users/form_update.html"
    model = Utilisateur
    form_class = UserActifForm
    success_url = reverse_lazy("Backend:AjouterUtilisateur")

    def form_valid(self, form):
        messages.success(self.request, "Modification effectuée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()

        context["a"] = a

        return context