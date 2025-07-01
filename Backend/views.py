import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
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
        membres = Membre.objects.all()
        context["a"] = a
        context["membres"] = membres
        return context


@method_decorator(permission_requise("creer role membre"), name='dispatch')
class CreateRoleMembre(CreateView):
    model = RoleMembre
    form_class = RoleMembreForm
    template_name = "admin/roleMembre/index.html"
    success_url = reverse_lazy("Backend:CreateRoleMembre")

    def form_valid(self, form):
        messages.success(self.request, "Le role a été créée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()
        role = RoleMembre.objects.all()
        context["a"] = a
        context["roles"] = role
        return context


@method_decorator(permission_requise("supprimer role membre"), name='dispatch')
class Supprimer_role_membre(DeleteView):
    model = RoleMembre
    template_name = 'admin/roleMembre/index.html'
    success_url = reverse_lazy('Backend:CreateRoleMembre')

    def form_valid(self, form):
        messages.success(self.request, "suppression effectuée avec succès !")
        return super().form_valid(form)


@method_decorator(permission_requise("modifier role membre"), name='dispatch')
class ModifierRoleMembre(UpdateView):
    template_name = "admin/roleMembre/form_partial.html"
    model = RoleMembre
    form_class = RoleMembreForm
    success_url = reverse_lazy("Backend:CreateRoleMembre")

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


@method_decorator(permission_requise("modifier membre"), name='dispatch')
class ModifierMembre(ModifierRoleMembre):
    template_name = "admin/membre_update.html"
    model = Membre
    form_class = MembreForm
    success_url = reverse_lazy("Backend:createMembre")


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


@method_decorator(permission_requise("supprimer membre"), name='dispatch')
class Supprimer_membre(Supprimer_role):
    model = Membre
    template_name = 'admin/CreationMembre.html'
    success_url = reverse_lazy('Backend:createMembre')


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
        context["utilisateurs"] = utilisateur

        return context


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


def retournerMembre(request):
    membre = Membre.objects.all()
    a = Association.objects.first()

    return render(request, 'admin/liste_membre.html', context={'membres': membre, "a":a})


@method_decorator(permission_requise("création de tontine"), name='dispatch')
class CreateTontine(CreationRoleUser):
    model = Tontine
    form_class = TontineForm
    template_name = "admin/tontine/Tontine.html"
    success_url = reverse_lazy("Backend:CreateTontine")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Association.objects.first()
        tontine = Tontine.objects.all()
        context["a"] = a
        context['tontine'] = tontine
        return context


@method_decorator(permission_requise("modification de tontine"), name='dispatch')
class SupprimerTontine(Supprimer_user):
    model = Tontine
    template_name = 'admin/tontine/Tontine.html'
    success_url = reverse_lazy('Backend:CreateTontine')


@method_decorator(permission_requise("suppression de tontine"), name='dispatch')
class ModifierTontine(ModifierUser):
    template_name = "admin/tontine/form_partial.html"
    model = Tontine
    form_class = TontineForm
    success_url = reverse_lazy("Backend:CreateTontine")


class SessionListCreateView(CreateView, ListView):
    model = SessionTontine
    form_class = SessionForm
    template_name = 'admin/tontine/sessions.html'
    context_object_name = 'sessions'

    def dispatch(self, request, *args, **kwargs):
        self.tontine = get_object_or_404(Tontine, pk=kwargs['tontine_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.tontine = self.tontine
        form.instance.status = True
        messages.success(self.request, "Creation effectuée avec succès !")
        return super().form_valid(form)

    def get_queryset(self):
        return SessionTontine.objects.filter(tontine=self.tontine)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tontine'] = self.tontine
        context['nbre'] = SessionTontine.objects.filter(status=True, tontine=self.tontine).count()
        context['form'] = self.get_form()
        context['a'] = Association.objects.first()
        return context

    def get_success_url(self):
        return reverse_lazy('Backend:sessions', kwargs={'tontine_id': self.tontine.id})


class SessionDeleteView(DeleteView):
    model = SessionTontine
    template_name = 'admin/tontine/sessions.html'

    def form_valid(self, form):
        messages.success(self.request, "Suppression effectuée avec succès !")
        return super().form_valid(form)

    def get_success_url(self):
        tontine_id = self.object.tontine.id
        return reverse_lazy('Backend:sessions', kwargs={'tontine_id': tontine_id})