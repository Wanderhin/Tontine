from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Association(models.Model):
    nom = models.CharField(max_length=50)
    slogan = models.CharField(max_length=50)
    description = models.TextField()
    dateCreation = models.DateField(blank=True)
    logo = models.ImageField(upload_to="logoAssociation")

    def save(self, *args, **kwargs):
        #self.dateCreation = datetime.today().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Association"


class Module(models.Model):
    nom = models.CharField(max_length=30)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Module"


class Permission(models.Model):
    permission = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.permission

    class Meta:
        verbose_name = "Permission"


class RoleUser(models.Model):
    role = models.CharField(max_length=30)
    description = models.TextField()
    permission = models.ManyToManyField(Permission)

    def __str__(self):
        return self.role

    def get_update_form(self):
        from Backend.formulaire import RoleUserForm
        return RoleUserForm(instance=self)

    class Meta:
        verbose_name = "Role des Utilisateur"


class RoleMembre(models.Model):
    role = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    def get_update_form(self):
        from Backend.formulaire import RoleMembreForm
        return RoleMembreForm(instance=self)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = "Role des Membre"


class Membre(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=60)
    localisation = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15)
    sexe = models.CharField(max_length=10)
    role = models.ForeignKey(RoleMembre, on_delete=models.SET_NULL, null=True)

    def get_update_form(self):
        from Backend.formulaire import MembreForm
        return MembreForm(instance=self)

    def __str__(self):
        return "{} {}".format(self.nom, self.prenom)

    class Meta:
        verbose_name = "Membre"


class Utilisateur(AbstractUser):
    photo = models.ImageField(upload_to="authentication")
    role = models.ForeignKey(RoleUser, on_delete=models.SET_NULL, null=True, blank=True)
    membre = models.OneToOneField(Membre, on_delete=models.SET_NULL, null=True, blank=True)
    association = models.OneToOneField(Association, on_delete=models.SET_NULL, null=True, blank=True)

    def get_update_form(self):
        from Backend.formulaire import UserActifForm
        return UserActifForm(instance=self)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utilisateur"


class Tontine(models.Model):
    intitule = models.CharField(max_length=150)
    description = models.TextField(verbose_name="Description de la tontine")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    frequence = models.CharField(max_length=20)
    montantPenalite = models.DecimalField(max_digits=10, decimal_places=2)
    association = models.ForeignKey(Association, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.intitule

    class Meta:
        verbose_name = "Tontine"

    def get_update_form(self):
            from Backend.formulaire import TontineForm
            return TontineForm(instance=self)


class SessionTontine(models.Model):
    intitule = models.CharField(max_length=150)
    tontine = models.ForeignKey(Tontine, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.intitule

    class Meta:
        verbose_name = "Session de tontine"


class ParametrageTontine(models.Model):
    dateDebut = models.DateField(verbose_name="Date de debut session")
    dateFin = models.DateField(verbose_name="date de fin de session")
    jourTirage = models.DateField(verbose_name="jour du tirage")
    jourCotisation = models.CharField(max_length=15, verbose_name="Jour de cotisation", default="lundi")
    typeTirage = models.CharField(max_length=150, verbose_name="type de tirage")
    periode = models.CharField(max_length=150, verbose_name="periode de cotisation")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    membre = models.ManyToManyField(Membre, verbose_name="selectionner tous les Membre Adherants")
    session = models.OneToOneField(SessionTontine, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.dateFin and self.dateDebut:
            self.dateFin = self.calculer_date_fin()
        super().save(*args, **kwargs)

    def calculer_date_fin(self):
        nombre_membres = self.membre.count() if self.pk else 0
        date_debut = self.dateDebut

        if self.periode == '1_semaine':
            delta = timedelta(weeks=nombre_membres)
        elif self.periode == '2_semaines':
            delta = timedelta(weeks=2 * nombre_membres)
        elif self.periode == '3_semaines':
            delta = timedelta(weeks=3 * nombre_membres)
        elif self.periode == '1_mois':
            delta = relativedelta(months=nombre_membres)
        elif self.periode == '3_mois':
            delta = relativedelta(months=3 * nombre_membres)
        elif self.periode == '6_mois':
            delta = relativedelta(months=6 * nombre_membres)
        elif self.periode == '1_an':
            delta = relativedelta(years=nombre_membres)
        else:
            delta = timedelta(weeks=nombre_membres)

        date_fin = date_debut + delta + timedelta(days=2)
        return date_fin

    def __str__(self):
        return str(self.session) if self.session else "Paramétrage sans session"

    class Meta:
        verbose_name = "Paramétrage"


class Cotisation(models.Model):
    date = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    etat = models.BooleanField(default=False)
    membre = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True)
    paramettrageTontine = models.ForeignKey(ParametrageTontine, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.today().date()
        if not self.montant and self.paramettrageTontine:
            self.montant = self.paramettrageTontine.montant
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.membre} - {self.montant}"

    class Meta:
        verbose_name = "Cotisation"


class Tirage(models.Model):
    numero = models.IntegerField(validators=[MinValueValidator(1)], help_text="valeur minimale est 1")
    membre = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True)
    paramettrageTontine = models.ForeignKey(ParametrageTontine, on_delete=models.SET_NULL, null=True)
    dateTirage = models.DateField()
    status = models.BooleanField(default=False, db_default=False)

    def save(self, *args, **kwargs):
        self.dateTirage = datetime.today().date()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tirage"


class Pret(models.Model):
    raison = models.CharField(max_length=250)
    dateEmprunt = models.DateField()
    dateRetourPrevu = models.DateField()
    dateRetour = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    membre = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True)
    paramettrageTontine = models.ForeignKey(ParametrageTontine, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False, )

    class Meta:
        verbose_name = "Prêt"
