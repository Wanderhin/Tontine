from django import forms
from Backend.models import Membre, Association, RoleUser, Utilisateur, RoleMembre, Tontine, SessionTontine, \
    ParametrageTontine, Cotisation
from django.contrib.auth.forms import UserCreationForm

sexes = (("masculin", "masculin"), ("feminin", "feminin"),)
tirage = (("aleatoire", "aleatoire"), ("manuellement", "manuellement"))
periodes = (("1_semaine", "cotisation chaque semaine"), ("2_semaines", "cotisation tout les 2 semaines"), ("3_semaines", "cotisation tout les 3 semaines"),
            ("1_mois", "cotisation tout les mois"), ("3_mois", "cotisation tout les 3 mois"), ("6_mois", "cotisation tout les 6 mois"), ("1_an", "cotisation tout les ans"))
jour = (("lundi","lundi"), ("mardi","mardi"), ("mercredi", "mercredi"), ("jeudi", "jeudi"),("vendredi", "vendredi"), ("samedi", "samedi"), ("dimanche","dimanche"))
taut = (("variable","taux variable"),("fixe", "taux fixe"))

class MembreForm(forms.ModelForm):
    sexe = forms.ChoiceField(choices=sexes)

    class Meta:
        model = Membre

        fields = ["nom", "prenom", "localisation", "telephone", "sexe", "role", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})  # Style Bootstrap


class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ['nom', 'slogan', 'description', 'logo', 'dateCreation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class RoleUserForm(forms.ModelForm):
    class Meta:
        model = RoleUser
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class UtilisateurForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password1', 'password2', 'photo', 'role', 'membre', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserActifForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'photo', 'role', 'membre', 'is_active', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class RoleMembreForm(forms.ModelForm):
    class Meta:
        model = RoleMembre
        fields = ['role', 'description', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TontineForm(forms.ModelForm):

    class Meta:
        model = Tontine
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class SessionForm(forms.ModelForm):
    class Meta:
        model = SessionTontine
        fields = ['intitule']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'status':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class ParametrageTontineForm(forms.ModelForm):
    periode = forms.ChoiceField(choices=periodes)
    typeTirage = forms.ChoiceField(choices=tirage)
    jourCotisation = forms.ChoiceField(choices=jour)
    taux = forms.ChoiceField(choices=taut)


    class Meta:
        model = ParametrageTontine
        fields = ['dateDebut', 'jourCotisation', 'jourTirage', 'typeTirage','taux', 'periode', 'montant', 'membre']
        widgets = {
            'dateDebut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'jourTirage': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.session:
            instance.session = self.session
        if commit:
            instance.save()
            self.save_m2m()
            # Recalculer la date de fin après avoir sauvé les membres
            instance.dateFin = instance.calculer_date_fin()
            instance.save()
        return instance

class CotisationForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ['status']
        widgets = {
            'status': forms.HiddenInput(),
        }

