from django import forms
from Backend.models import Membre, Association, RoleUser, Utilisateur, RoleMembre, Tontine, SessionTontine
from django.contrib.auth.forms import UserCreationForm

sexes = (("masculin", "masculin"), ("feminin", "feminin"),)
tirage = (("aleatoire", "aleatoire"), ("manuellement", "manuellement"))


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