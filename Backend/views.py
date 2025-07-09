import calendar
import datetime
import random

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
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

    return render(request, 'admin/liste_membre.html', context={'membres': membre, "a": a})


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


@method_decorator(permission_requise("supprimer tontine"), name='dispatch')
class SupprimerTontine(Supprimer_user):
    model = Tontine
    template_name = 'admin/tontine/Tontine.html'
    success_url = reverse_lazy('Backend:CreateTontine')


@method_decorator(permission_requise("modification de tontine"), name='dispatch')
class ModifierTontine(ModifierUser):
    template_name = "admin/tontine/form_partial.html"
    model = Tontine
    form_class = TontineForm
    success_url = reverse_lazy("Backend:CreateTontine")


@method_decorator(permission_requise("gerer session"), name='dispatch')
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


@method_decorator(permission_requise("modification de tontine"), name='dispatch')
class SessionDeleteView(DeleteView):
    model = SessionTontine
    template_name = 'admin/tontine/sessions.html'

    def form_valid(self, form):
        messages.success(self.request, "Suppression effectuée avec succès !")
        return super().form_valid(form)

    def get_success_url(self):
        tontine_id = self.object.tontine.id
        return reverse_lazy('Backend:sessions', kwargs={'tontine_id': tontine_id})


class ParametrageTontineCreateView(CreateView):
    model = ParametrageTontine
    form_class = ParametrageTontineForm
    template_name = 'admin/tontine/parametrage_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        session_id = self.kwargs.get('session_id')
        if session_id:
            kwargs['session'] = get_object_or_404(SessionTontine, id=session_id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.kwargs.get('session_id')

        context['a'] = Association.objects.first()
        if session_id:
            context['session'] = get_object_or_404(SessionTontine, id=session_id)
            # Récupérer les paramétrages existants pour cette session
            context['parametrages'] = ParametrageTontine.objects.filter(session_id=session_id)
            context['nbreParametrage'] = ParametrageTontine.objects.filter(session_id=session_id).count()
        return context

    def get_success_url(self):
        return reverse('Backend:parametrage_create', kwargs={'session_id': self.object.session.id})

    def form_valid(self, form):
        messages.success(self.request, "Creation effectuée avec succès !")
        return super().form_valid(form)


class CotisationListView(DetailView):
    model = ParametrageTontine
    template_name = 'admin/tontine/cotisation_list.html'
    context_object_name = 'parametrage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parametrage = self.get_object()
        user = self.request.user
        # Générer les cotisations si nécessaire
        self.generer_cotisations_si_necessaire(parametrage)

        # Récupérer les cotisations en attente (etat=False)
        cotisations_en_attente = Cotisation.objects.filter(
            paramettrageTontine=parametrage,
            etat=False
        ).order_by('date', 'membre__nom')

        context['cotisations'] = cotisations_en_attente
        context['peut_traiter'] = self.peut_traiter_cotisations(parametrage)
        context['a'] = Association.objects.first()
        context['cotisation_terminer'] = Cotisation.objects.filter(paramettrageTontine=parametrage,
                                                                   etat=True).order_by('date', 'membre__nom')
        context['cotisation_terminer_user'] = Cotisation.objects.filter(paramettrageTontine=parametrage,
                                                                        etat=True, membre=user.membre).order_by('date',
                                                                                                                'membre__nom')

        return context

    def generer_cotisations_si_necessaire(self, parametrage):
        """Génère les cotisations pour la période courante si nécessaire"""
        aujourd_hui = timezone.now().date()

        # Calculer la prochaine date de cotisation
        prochaine_date = self.calculer_prochaine_date_cotisation(parametrage, aujourd_hui)

        if prochaine_date and prochaine_date <= aujourd_hui:
            # Vérifier si des cotisations existent déjà pour cette période
            cotisations_existantes = Cotisation.objects.filter(
                paramettrageTontine=parametrage,
                date=prochaine_date
            ).exists()

            if not cotisations_existantes:
                # Créer les cotisations pour tous les membres
                for membre in parametrage.membre.all():
                    # Si le taux est variable, ne pas définir de montant fixe
                    montant_cotisation = None if parametrage.taux == 'variable' else parametrage.montant

                    Cotisation.objects.create(
                        date=prochaine_date,
                        montant=montant_cotisation,
                        membre=membre,
                        paramettrageTontine=parametrage
                    )

    def calculer_prochaine_date_cotisation(self, parametrage, date_reference):
        """Calcule la prochaine date de cotisation basée sur la période et le jour"""
        jours_semaine = {
            'lundi': 0, 'mardi': 1, 'mercredi': 2, 'jeudi': 3,
            'vendredi': 4, 'samedi': 5, 'dimanche': 6
        }

        jour_cotisation = jours_semaine.get(parametrage.jourCotisation.lower())
        if jour_cotisation is None:
            return None

        date_debut = parametrage.dateDebut
        date_fin = parametrage.dateFin

        if date_reference < date_debut or date_reference > date_fin:
            return None

        # Calculer la date de cotisation pour la période courante
        if parametrage.periode == '1_semaine':
            # Trouver le dernier jour de cotisation de la semaine
            jours_depuis_debut = (date_reference - date_debut).days
            semaines_ecoulees = jours_depuis_debut // 7
            date_cotisation = date_debut + timedelta(weeks=semaines_ecoulees)

            # Ajuster au bon jour de la semaine
            while date_cotisation.weekday() != jour_cotisation:
                date_cotisation += timedelta(days=1)

        elif parametrage.periode == '2_semaines':
            # Calcul par cycles de 2 semaines
            jours_depuis_debut = (date_reference - date_debut).days
            cycles_ecoules = jours_depuis_debut // 14
            date_cycle_debut = date_debut + timedelta(weeks=cycles_ecoules * 2)

            # Trouver le jour de cotisation dans ce cycle de 2 semaines
            date_cotisation = date_cycle_debut
            while date_cotisation.weekday() != jour_cotisation:
                date_cotisation += timedelta(days=1)

            # Si le jour de cotisation est passé dans ce cycle, prendre le suivant
            if date_cotisation < date_reference:
                date_cotisation += timedelta(weeks=2)

        elif parametrage.periode == '3_semaines':
            # Calcul par cycles de 3 semaines
            jours_depuis_debut = (date_reference - date_debut).days
            cycles_ecoules = jours_depuis_debut // 21
            date_cycle_debut = date_debut + timedelta(weeks=cycles_ecoules * 3)

            # Trouver le jour de cotisation dans ce cycle de 3 semaines
            date_cotisation = date_cycle_debut
            while date_cotisation.weekday() != jour_cotisation:
                date_cotisation += timedelta(days=1)

            # Si le jour de cotisation est passé dans ce cycle, prendre le suivant
            if date_cotisation < date_reference:
                date_cotisation += timedelta(weeks=3)

        elif parametrage.periode == '1_mois':
            # Trouver le dernier jour de cotisation du mois
            annee = date_reference.year
            mois = date_reference.month

            # Dernier jour du mois
            dernier_jour = calendar.monthrange(annee, mois)[1]

            # Trouver le dernier jour de cotisation du mois
            for jour in range(dernier_jour, 0, -1):
                date_test = datetime(annee, mois, jour).date()
                if date_test.weekday() == jour_cotisation:
                    date_cotisation = date_test
                    break
            else:
                return None

        elif parametrage.periode == '3_mois':
            # Calcul par trimestres
            # Calculer le nombre de trimestres depuis le début
            mois_depuis_debut = (date_reference.year - date_debut.year) * 12 + (date_reference.month - date_debut.month)
            trimestres_ecoules = mois_depuis_debut // 3

            # Date de début du trimestre courant
            date_trimestre_debut = date_debut + relativedelta(months=trimestres_ecoules * 3)

            # Trouver le dernier jour de cotisation du trimestre
            date_fin_trimestre = date_trimestre_debut + relativedelta(months=3, days=-1)

            # Chercher le dernier jour de cotisation dans le trimestre
            date_cotisation = None
            date_courante = date_fin_trimestre

            while date_courante >= date_trimestre_debut:
                if date_courante.weekday() == jour_cotisation:
                    date_cotisation = date_courante
                    break
                date_courante -= timedelta(days=1)

            # Si pas trouvé ou si la date est passée, prendre le prochain trimestre
            if date_cotisation is None or date_cotisation < date_reference:
                date_trimestre_suivant = date_trimestre_debut + relativedelta(months=3)
                date_fin_trimestre_suivant = date_trimestre_suivant + relativedelta(months=3, days=-1)

                date_courante = date_fin_trimestre_suivant
                while date_courante >= date_trimestre_suivant:
                    if date_courante.weekday() == jour_cotisation:
                        date_cotisation = date_courante
                        break
                    date_courante -= timedelta(days=1)

        elif parametrage.periode == '6_mois':
            # Calcul par semestres
            # Calculer le nombre de semestres depuis le début
            mois_depuis_debut = (date_reference.year - date_debut.year) * 12 + (date_reference.month - date_debut.month)
            semestres_ecoules = mois_depuis_debut // 6

            # Date de début du semestre courant
            date_semestre_debut = date_debut + relativedelta(months=semestres_ecoules * 6)

            # Trouver le dernier jour de cotisation du semestre
            date_fin_semestre = date_semestre_debut + relativedelta(months=6, days=-1)

            # Chercher le dernier jour de cotisation dans le semestre
            date_cotisation = None
            date_courante = date_fin_semestre

            while date_courante >= date_semestre_debut:
                if date_courante.weekday() == jour_cotisation:
                    date_cotisation = date_courante
                    break
                date_courante -= timedelta(days=1)

            # Si pas trouvé ou si la date est passée, prendre le prochain semestre
            if date_cotisation is None or date_cotisation < date_reference:
                date_semestre_suivant = date_semestre_debut + relativedelta(months=6)
                date_fin_semestre_suivant = date_semestre_suivant + relativedelta(months=6, days=-1)

                date_courante = date_fin_semestre_suivant
                while date_courante >= date_semestre_suivant:
                    if date_courante.weekday() == jour_cotisation:
                        date_cotisation = date_courante
                        break
                    date_courante -= timedelta(days=1)

        elif parametrage.periode == '1_an':
            # Calcul par années
            # Calculer le nombre d'années depuis le début
            annees_ecoulees = date_reference.year - date_debut.year

            # Date de début de l'année courante du cycle
            date_annee_debut = date_debut + relativedelta(years=annees_ecoulees)

            # Trouver le dernier jour de cotisation de l'année
            date_fin_annee = date_annee_debut + relativedelta(years=1, days=-1)

            # Chercher le dernier jour de cotisation dans l'année
            date_cotisation = None
            date_courante = date_fin_annee

            while date_courante >= date_annee_debut:
                if date_courante.weekday() == jour_cotisation:
                    date_cotisation = date_courante
                    break
                date_courante -= timedelta(days=1)

            # Si pas trouvé ou si la date est passée, prendre l'année suivante
            if date_cotisation is None or date_cotisation < date_reference:
                date_annee_suivante = date_annee_debut + relativedelta(years=1)
                date_fin_annee_suivante = date_annee_suivante + relativedelta(years=1, days=-1)

                date_courante = date_fin_annee_suivante
                while date_courante >= date_annee_suivante:
                    if date_courante.weekday() == jour_cotisation:
                        date_cotisation = date_courante
                        break
                    date_courante -= timedelta(days=1)

        else:
            # Période non supportée
            return None

        # Vérifier que la date calculée est dans la plage autorisée
        if date_cotisation and date_cotisation <= date_fin:
            return date_cotisation
        else:
            return None

    def peut_traiter_cotisations(self, parametrage):
        """Vérifie si on peut encore traiter les cotisations (dans les 2 jours)"""
        aujourd_hui = timezone.now().date()

        # Récupérer la dernière date de cotisation
        derniere_cotisation = Cotisation.objects.filter(
            paramettrageTontine=parametrage,
            etat=False
        ).first()

        if derniere_cotisation:
            date_limite = derniere_cotisation.date + timedelta(days=2)
            return aujourd_hui <= date_limite

        return False


def traiter_cotisation(request, cotisation_id, action):
    """Traite une cotisation (succès ou échec) avec gestion des montants variables"""
    cotisation = get_object_or_404(Cotisation, id=cotisation_id)
    a = Association.objects.first()

    # Vérifier si on peut encore traiter cette cotisation
    if not peut_traiter_cotisation(cotisation):
        messages.error(request, "La période de traitement de cette cotisation est terminée.")
        return redirect('Backend:cotisation_list', pk=cotisation.paramettrageTontine.id)

    if action == 'reussir':
        # Vérifier si c'est une cotisation à montant variable
        if cotisation.paramettrageTontine.taux == 'variable':
            # Récupérer le montant depuis les données POST
            montant = request.POST.get('montant', '').strip()

            if not montant:
                messages.error(request, "Veuillez saisir le montant de la cotisation.")
                return redirect('Backend:cotisation_list', pk=cotisation.paramettrageTontine.id)

            try:
                montant_float = float(montant.replace(',', '.'))
                if montant_float <= 0:
                    messages.error(request, "Le montant doit être positif.")
                    return redirect('Backend:cotisation_list', pk=cotisation.paramettrageTontine.id)

                # Mettre à jour le montant
                cotisation.montant = montant_float

            except ValueError:
                messages.error(request, "Montant invalide. Veuillez saisir un nombre valide.")
                return redirect('Backend:cotisation_list', pk=cotisation.paramettrageTontine.id)

        cotisation.status = True
        cotisation.etat = True
        message = f"Cotisation de {cotisation.membre} marquée comme réussie"

        # Ajouter le montant dans le message si c'est variable
        if cotisation.paramettrageTontine.taux == 'variable':
            message += f" (Montant: {cotisation.montant:,.0f} FCFA)"

    elif action == 'echouer':
        # Pour les échecs, on peut optionnellement enregistrer une raison
        raison = request.POST.get('raison', '').strip()

        cotisation.status = False
        cotisation.etat = True

        # Si vous avez un champ pour la raison d'échec, l'enregistrer
        if hasattr(cotisation, 'raison_echec') and raison:
            cotisation.raison_echec = raison

        message = f"Cotisation de {cotisation.membre} marquée comme échouée"
        if raison:
            message += f" (Raison: {raison})"

    else:
        messages.error(request, "Action invalide")
        return redirect('Backend:cotisation_list', pk=cotisation.paramettrageTontine.id)

    cotisation.save()
    messages.success(request, message)

    # Vérifier si toutes les cotisations de la période sont traitées
    cotisations_non_traitees = Cotisation.objects.filter(
        paramettrageTontine=cotisation.paramettrageTontine,
        date=cotisation.date,
        etat=False
    ).count()

    if cotisations_non_traitees == 0:
        # Calculer les statistiques de la période
        cotisations_periode = Cotisation.objects.filter(
            paramettrageTontine=cotisation.paramettrageTontine,
            date=cotisation.date
        )

        total_reussies = cotisations_periode.filter(status=True).count()
        total_echouees = cotisations_periode.filter(status=False).count()

        # Calculer le montant total collecté pour cette période
        montant_total = cotisations_periode.filter(status=True).aggregate(
            total=models.Sum('montant')
        )['total'] or 0

        messages.info(request,
                      f"Période du {cotisation.date.strftime('%d/%m/%Y')} terminée: "
                      f"{total_reussies} réussies, {total_echouees} échouées. "
                      f"Montant total collecté: {montant_total:,.0f} FCFA"
                      )

        # Vérifier si la session est terminée
        if timezone.now().date() >= cotisation.paramettrageTontine.dateFin:
            session = cotisation.paramettrageTontine.session
            session.status = False
            session.save()

            # Calculer les statistiques finales de la session
            stats_session = calculer_statistiques_session(cotisation.paramettrageTontine)
            messages.info(request,
                          f"Session terminée automatiquement. "
                          f"Statistiques finales: {stats_session}"
                          )

    return redirect('Backend:cotisation_list', pk=cotisation.paramettrageTontine.id)


def peut_traiter_cotisation(cotisation):
    """Vérifie si une cotisation peut encore être traitée"""
    aujourd_hui = timezone.now().date()

    # Vérifier si la cotisation n'est pas déjà traitée
    if cotisation.etat:
        return False

    # Vérifier la limite de 2 jours après la date de cotisation
    date_limite = cotisation.date + timedelta(days=2)
    return aujourd_hui <= date_limite


def calculer_statistiques_session(parametrage):
    """Calcule les statistiques d'une session de tontine"""
    toutes_cotisations = Cotisation.objects.filter(paramettrageTontine=parametrage)

    total_cotisations = toutes_cotisations.count()
    cotisations_reussies = toutes_cotisations.filter(status=True).count()
    cotisations_echouees = toutes_cotisations.filter(status=False).count()

    montant_total = toutes_cotisations.filter(status=True).aggregate(
        total=models.Sum('montant')
    )['total'] or 0

    taux_reussite = (cotisations_reussies / total_cotisations * 100) if total_cotisations > 0 else 0

    return (
        f"Total: {total_cotisations}, "
        f"Réussies: {cotisations_reussies}, "
        f"Échouées: {cotisations_echouees}, "
        f"Taux de réussite: {taux_reussite:.1f}%, "
        f"Montant total: {montant_total:,.0f} FCFA"
    )


# Fonction pour traiter plusieurs cotisations en lot
def traiter_cotisations_lot(request, parametrage_id):
    """Traite plusieurs cotisations en lot avec gestion des montants variables"""
    parametrage = get_object_or_404(ParametrageTontine, id=parametrage_id)

    if request.method == 'POST':
        cotisations_ids = request.POST.getlist('cotisations_ids')
        action = request.POST.get('action')

        if not cotisations_ids:
            messages.error(request, "Aucune cotisation sélectionnée.")
            return redirect('Backend:cotisation_list', pk=parametrage_id)

        cotisations = Cotisation.objects.filter(
            id__in=cotisations_ids,
            paramettrageTontine=parametrage,
            etat=False
        )

        if action == 'reussir':
            return traiter_cotisations_lot_reussir(request, cotisations, parametrage)
        elif action == 'echouer':
            return traiter_cotisations_lot_echouer(request, cotisations, parametrage)
        else:
            messages.error(request, "Action invalide.")

    return redirect('Backend:cotisation_list', pk=parametrage_id)


def traiter_cotisations_lot_reussir(request, cotisations, parametrage):
    """Traite un lot de cotisations comme réussies"""
    cotisations_traitees = 0
    erreurs = []

    for cotisation in cotisations:
        if not peut_traiter_cotisation(cotisation):
            erreurs.append(f"Période expirée pour {cotisation.membre}")
            continue

        # Gérer les montants variables
        if parametrage.taux == 'variable':
            montant_key = f'montant_{cotisation.id}'
            montant = request.POST.get(montant_key, '').strip()

            if not montant:
                erreurs.append(f"Montant manquant pour {cotisation.membre}")
                continue

            try:
                montant_float = float(montant.replace(',', '.'))
                if montant_float <= 0:
                    erreurs.append(f"Montant invalide pour {cotisation.membre}")
                    continue

                cotisation.montant = montant_float

            except ValueError:
                erreurs.append(f"Montant invalide pour {cotisation.membre}")
                continue

        cotisation.status = True
        cotisation.etat = True
        cotisation.save()
        cotisations_traitees += 1

    # Messages de retour
    if cotisations_traitees > 0:
        messages.success(request, f"{cotisations_traitees} cotisation(s) traitée(s) avec succès.")

    if erreurs:
        messages.error(request, "Erreurs: " + "; ".join(erreurs))

    return redirect('Backend:cotisation_list', pk=parametrage.id)


def traiter_cotisations_lot_echouer(request, cotisations, parametrage):
    """Traite un lot de cotisations comme échouées"""
    cotisations_traitees = 0
    raison = request.POST.get('raison_echec', '').strip()

    for cotisation in cotisations:
        if not peut_traiter_cotisation(cotisation):
            continue

        cotisation.status = False
        cotisation.etat = True

        # Enregistrer la raison d'échec si le champ existe
        if hasattr(cotisation, 'raison_echec') and raison:
            cotisation.raison_echec = raison

        cotisation.save()
        cotisations_traitees += 1

    if cotisations_traitees > 0:
        message = f"{cotisations_traitees} cotisation(s) marquée(s) comme échouée(s)."
        if raison:
            message += f" Raison: {raison}"
        messages.success(request, message)

    return redirect('Backend:cotisation_list', pk=parametrage.id)


def marquer_cotisations_automatiquement(request):
    """Marque automatiquement les cotisations non traitées comme échec après 2 jours"""
    aujourd_hui = timezone.now().date()

    # Récupérer toutes les cotisations non traitées dépassant 2 jours
    cotisations_a_traiter = Cotisation.objects.filter(
        etat=False,
        date__lt=aujourd_hui - timedelta(days=2)
    )

    count = 0
    for cotisation in cotisations_a_traiter:
        cotisation.status = False
        cotisation.etat = True
        cotisation.save()
        count += 1

    return JsonResponse({'message': f'{count} cotisations marquées automatiquement comme échec'})


def tirage_view(request, parametrage_id):
    """Vue principale pour le tirage - détermine le type de tirage"""
    parametrage = get_object_or_404(ParametrageTontine, id=parametrage_id)

    # Vérifier si des tirages existent déjà
    tirages_existants = Tirage.objects.filter(paramettrageTontine=parametrage).exists()

    if tirages_existants:
        i = 0


    # Rediriger selon le type de tirage
    if parametrage.typeTirage.lower() == 'manuellement':
        return redirect('Backend:tirage_manuel', parametrage_id=parametrage_id)
    elif parametrage.typeTirage.lower() == 'aleatoire':
        return redirect('Backend:tirage_automatique', parametrage_id=parametrage_id)
    else:
        return None


def tirage_manuel(request, parametrage_id):
    """Vue pour le tirage manuel"""
    parametrage = get_object_or_404(ParametrageTontine, id=parametrage_id)
    membres = parametrage.membre.all()
    a = Association.objects.first()
    # Vérifier si des tirages existent déjà
    tirages_existants = Tirage.objects.filter(paramettrageTontine=parametrage)

    if tirages_existants.exists():
        messages.warning(request, "Des tirages existent déjà pour ce paramétrage.")
        return redirect('Backend:listeTirageManuelle', parametrage_id)

    context = {
        'parametrage': parametrage,
        'membres': membres,
        'nombre_membres': membres.count(),
        'numeros_disponibles': list(range(1, membres.count() + 1)),
         "a": a,
    }

    return render(request, 'admin/tontine/tirage_manuel.html', context)


def tirage_automatique(request, parametrage_id):
    """Vue pour le tirage automatique"""
    parametrage = get_object_or_404(ParametrageTontine, id=parametrage_id)
    membres = parametrage.membre.all()
    a = Association.objects.first()

    # Vérifier si des tirages existent déjà
    tirages_existants = Tirage.objects.filter(paramettrageTontine=parametrage)

    if tirages_existants.exists():
        messages.success(request, "Des tirages existent déjà pour ce paramétrage.")
        return redirect('Backend:listeTirageAutomatique', parametrage_id)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Créer une liste de numéros et la mélanger
                numeros = list(range(1, membres.count() + 1))
                random.shuffle(numeros)

                # Créer les tirages
                for i, membre in enumerate(membres):
                    Tirage.objects.create(
                        numero=numeros[i],
                        membre=membre,
                        paramettrageTontine=parametrage
                    )

                messages.success(request, "Tirage automatique effectué avec succès!")
                return redirect('Backend:parametrage_create',session_id=parametrage.session_id)

        except Exception as e:
            messages.error(request, f"Erreur lors du tirage automatique : {str(e)}")

    # Afficher la prévisualisation
    membres_list = list(membres)
    numeros = list(range(1, len(membres_list) + 1))
    random.shuffle(numeros)

    preview = list(zip(membres_list, numeros))

    context = {
        'parametrage': parametrage,
        'membres': membres,
        'nombre_membres': membres.count(),
        'preview': preview
        , "a": a
    }

    return render(request, 'admin/tontine/tirage_automatique.html', context)


def sauvegarder_tirage_manuel(request, parametrage_id):
    """Sauvegarde le tirage manuel"""
    if request.method != 'POST':
        return redirect('Backend:tirage_manuel', parametrage_id=parametrage_id)

    parametrage = get_object_or_404(ParametrageTontine, id=parametrage_id)
    membres = parametrage.membre.all()

    # Vérifier si des tirages existent déjà
    tirages_existants = Tirage.objects.filter(paramettrageTontine=parametrage)

    if tirages_existants.exists():
        messages.warning(request, "Des tirages existent déjà pour ce paramétrage.")
        return redirect('Backend:parametrage_create', parametrage_id=parametrage_id)

    try:
        with transaction.atomic():
            numeros_utilises = []

            for membre in membres:
                numero_key = f'numero_{membre.id}'
                numero = request.POST.get(numero_key)

                if not numero:
                    messages.error(request, f"Numéro manquant pour le membre {membre.nom}")
                    return redirect('Backend:tirage_manuel', parametrage_id=parametrage_id)

                try:
                    numero = int(numero)
                except ValueError:
                    messages.error(request, f"Numéro invalide pour le membre {membre.nom}")
                    return redirect('Backend:tirage_manuel', parametrage_id=parametrage_id)

                # Vérifier que le numéro est dans la plage valide
                if numero < 1 or numero > membres.count():
                    messages.error(request, f"Le numéro pour {membre.nom} doit être entre 1 et {membres.count()}")
                    return redirect('Backend:tirage_manuel', parametrage_id=parametrage_id)

                # Vérifier que le numéro n'est pas déjà utilisé
                if numero in numeros_utilises:
                    messages.error(request, f"Le numéro {numero} est déjà utilisé")
                    return redirect('Backend:tirage_manuel', parametrage_id=parametrage_id)

                numeros_utilises.append(numero)

                # Créer le tirage
                Tirage.objects.create(
                    numero=numero,
                    membre=membre,
                    paramettrageTontine=parametrage
                )

            messages.success(request, "Tirage manuel sauvegardé avec succès!")
            return redirect('Backend:parametrage_create', parametrage_id=parametrage_id)

    except Exception as e:
        messages.error(request, f"Erreur lors de la sauvegarde : {str(e)}")
        return redirect('Backend:tirage_manuel', parametrage_id=parametrage_id)


def listeTirageManuelle(request, parametrage_id):
    liste = Tirage.objects.filter(paramettrageTontine_id=parametrage_id)
    parametrage = get_object_or_404(ParametrageTontine, id=parametrage_id)
    a = Association.objects.first()
    membres = parametrage.membre.all()
    return render(request, "admin/tontine/listeTirage.html", context={"listes": liste, "parametrage": parametrage, "a": a, 'nombre_membres': membres.count()})


def listeTirageAutomatique(request, parametrage_id):
    liste = Tirage.objects.filter(paramettrageTontine_id=parametrage_id)
    parametrage = get_object_or_404(ParametrageTontine, id=parametrage_id)
    membres = parametrage.membre.all()
    return render(request, "admin/tontine/listeTirageAutomatique.html", context={"listes": liste, "parametrage": parametrage, 'nombre_membres': membres.count()})
