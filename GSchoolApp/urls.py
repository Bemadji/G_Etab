from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.messages.context_processors import messages
from django.conf.urls import handler404

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('eleves/', views.liste_eleves, name='liste_eleves'), # URL pour la liste des élèves
    path('eleves/<int:eleve_id>/', views.detail_eleve, name='detail_eleve'), # URL pour le détail d'un élève
    path('emploi_du_temps/', views.emploi_du_temps, name='emploi_du_temps'), # URL pour l'emploi du temps
    path('matieres/', views.liste_matieres, name='liste_matieres'), # URL pour la liste des matières
    path('matieres/<int:matiere_id>/', views.detail_matiere, name='detail_matiere'), # URL pour le détail d'une 
    path('eleves/<int:eleve_id>/bulletins/', views.bulletins_eleve, name='bulletin_eleve'),    
    path('bulletins/<int:bulletin_id>/', views.detail_bulletin, name='detail_bulletin'),# URL pour le détail d'un bulletin
    path('absences/', views.liste_absences, name='liste_absences'),# URL pour la liste des absences
    path('eleve/<int:eleve_id>/liste_notes/', views.liste_notes_eleve, name='liste_notes_eleve'),# URL pour la liste des notes
    path('liste_notes/', views.liste_notes, name='liste_notes'),
    path('classes/', views.liste_classes, name='liste_classes'),
    path('classes/<int:classe_id>/', views.detail_classe, name='detail_classe'),  # URL pour les détails de la classe
    path('contact', views.contact, name='contact'),
    path('evaluations/', views.liste_evaluations, name='liste_evaluations'),
    path('evaluations/<int:evaluation_id>/', views.detail_evaluation, name='detail_evaluation'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('inscription/', views.register_view, name='inscription'),
    path('enseignants/', views.liste_enseignant, name='liste_enseignant'),
    path('enseignants/<int:id>/', views.detail_enseignant, name='detail_enseignant'),
    path('annees-scolaires/', views.liste_annees_scolaires, name='liste_annees_scolaires'),
    path('annees-scolaires/<int:annee_scolaire_id>/', views.detail_annee_scolaire, name='detail_annee_scolaire'),
    path('about/', views.about_page, name='about_page'),
    path('classe/<int:classe_id>/notes/', views.afficher_notes_par_classe, name='afficher_notes_par_classe'),# URL pour afficher les notes par classe
    path('eleve/<int:eleve_id>/ajouter_note/', views.ajouter_note, name='ajouter_note'),# URL pour ajouter une note à un élève

]

#handler404 = "helpers.views.handle_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)