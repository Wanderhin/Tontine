from django.urls import path, include
from django.contrib.auth import views
from .views import *
app_name = "Backend"
urlpatterns = [

    path('', CustomLoginView.as_view(), name="login"),
    path('', views.LogoutView.as_view(), name="logout"),
    path('gestion des roles', CreationRoleUser.as_view(), name="CreationRoleUser"),
    path('accueil/', home, name="home"),
    path('gerer les tontines/', CreateTontine.as_view(), name="CreateTontine"),
    path('liste des membres/', retournerMembre, name="liste_membre"),
    path('ajout-membre/', CreateMembre.as_view(), name='createMembre'),
    path('ajout-role-Membre/', CreateRoleMembre.as_view(), name='CreateRoleMembre'),
    path('ajout-utilisateur/', AjouterUtilisateur.as_view(), name='AjouterUtilisateur'),
    path('marquer-automatique/', marquer_cotisations_automatiquement, name='marquer_automatique'),
    path('association/<int:pk>', ParamettrageAssociation.as_view(), name="modification_asso"),
    path('supprimer role/<int:pk>/', Supprimer_role.as_view(), name="supprimer_role"),
    path('modifier role utilisateur/<int:pk>/', ModifierRoleUser.as_view(), name="modifier_role"),
    path('modifier utilisateur/<int:pk>/', ModifierUser.as_view(), name="modifier_user"),
    path('supprimer un utilisateur/<int:pk>/', Supprimer_user.as_view(), name="supprimer_user"),
    path('modifier un role/<int:pk>/', ModifierRoleMembre.as_view(), name="modifier_role_membre"),
    path('supprimer un role de membre/<int:pk>/', Supprimer_role_membre.as_view(), name="supprimer_role_membre"),
    path('modifier un membre/<int:pk>/', ModifierMembre.as_view(), name="modifier_membre"),
    path('supprimer un membre/<int:pk>/', Supprimer_membre.as_view(), name="supprimer_membre"),
    path('modifier une tontine/<int:pk>/', ModifierTontine.as_view(), name="modifier_tontine"),
    path('supprimer un membre/<int:pk>/', SupprimerTontine.as_view(), name="supprimer_tontine"),
    path('<int:tontine_id>/sessionDeTontine/', SessionListCreateView.as_view(), name='sessions'),
    path('session/<int:pk>/supprimer/', SessionDeleteView.as_view(), name='session_delete'),
    path('parametrage/create/<int:session_id>/', ParametrageTontineCreateView.as_view(), name='parametrage_create'),
    # Gestion des cotisations
    path('cotisations/<int:pk>/', CotisationListView.as_view(), name='cotisation_list'),
    path('cotisation/<int:cotisation_id>/<str:action>/', traiter_cotisation, name='traiter_cotisation'),


]