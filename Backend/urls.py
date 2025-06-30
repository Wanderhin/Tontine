from django.urls import path, include
from django.contrib.auth import views
from .views import *
app_name = "Backend"
urlpatterns = [

    path('', CustomLoginView.as_view(), name="login"),
    path('', views.LogoutView.as_view(), name="logout"),
    path('gestion des roles', CreationRoleUser.as_view(), name="CreationRoleUser"),
    path('accueil/', home, name="home"),
    path('ajout-membre/', CreateMembre.as_view(), name='createMembre'),
    path('ajout-utilisateur/', AjouterUtilisateur.as_view(), name='AjouterUtilisateur'),
    path('association/<int:pk>', ParamettrageAssociation.as_view(), name="modification_asso"),
    path('supprimer role/<int:pk>/', Supprimer_role.as_view(), name="supprimer_role"),
    path('modifier role utilisateur/<int:pk>/', ModifierRoleUser.as_view(), name="modifier_role"),
    path('modifier utilisateur/<int:pk>/', ModifierUser.as_view(), name="modifier_user"),
    path('supprimer un utilisateur/<int:pk>/', Supprimer_user.as_view(), name="supprimer_user"),
]