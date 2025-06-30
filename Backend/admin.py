from django.contrib import admin

from Backend.models import *


class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("username", "password", "email", "photo", "is_active", "is_superuser",)
    list_display_links = ("username",)
    search_fields = ['username', ]
    list_filter = ("username",)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):  # Vérifie si un mot de passe est fourni
            obj.set_password(form.cleaned_data['password'])  # Hacher le mot de passe
        super().save_model(request, obj, form, change)


class RoleUserAdmin(admin.ModelAdmin):
    list_display = ("role",)
    list_display_links = ("role",)


class AssociationAdmin(admin.ModelAdmin):
    list_display = ("pk","nom", "slogan", "description", "logo", "dateCreation",)
    list_display_links = ("nom",)


class ModuleAdmin(admin.ModelAdmin):
    list_display = ("nom", "description",)
    list_display_links = ("nom",)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ("permission", "description", "module",)
    list_display_links = ("permission",)


class RoleMembreAdmin(admin.ModelAdmin):
    list_display = ("role", "description",)
    list_display_links = ("role",)


class MembreAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "localisation", "telephone", "role",)
    list_display_links = ("nom",)


class TontineAdmin(admin.ModelAdmin):
    list_display = ("intitule", "montant", "description", "frequence", "montantPenalite", "association")
    list_display_links = ("intitule",)


class PeriodeAdmin(admin.ModelAdmin):
    list_display = ("periode", "nomComplet",)
    list_display_links = ("periode",)


class SessionAdmin(admin.ModelAdmin):
    list_display = ("intitule", "tontine", "status",)
    list_display_links = ("intitule",)


class ParamettrageAdmin(admin.ModelAdmin):
    list_display = ("tontine", "session", "periode", "typeTirage", "dateDebut", "dateFin", "jourTirage", "jourBouffe")
    list_display_links = ("tontine",)


class CotisationAdmin(admin.ModelAdmin):
    list_display = ("membre", "paramettrageTontine", "montant", "date", "etat", "status",)
    list_display_links = ("membre", "paramettrageTontine",)
    search_fields = ["paramettrageTontine", ]
    list_filter = ("membre", "paramettrageTontine", "montant", "date", 'etat', "status",)
    list_per_page = 50


class PretAdmin(admin.ModelAdmin):
    list_display = ("membre", "paramettrageTontine", "montant", "dateEmprunt", "dateRetour",)
    list_display_links = ("membre",)


admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(RoleUser, RoleUserAdmin)
admin.site.register(Association, AssociationAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(RoleMembre, RoleMembreAdmin)
admin.site.register(Membre, MembreAdmin)
admin.site.register(Tontine, TontineAdmin)
admin.site.register(Periode, PeriodeAdmin)
admin.site.register(SessionTontine, SessionAdmin)
admin.site.register(ParametrageTontine, ParamettrageAdmin)
admin.site.register(Cotisation, CotisationAdmin)
admin.site.register(Pret, PretAdmin)
