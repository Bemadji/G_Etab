from django.contrib import admin
from GSchoolApp.models import Absence, Annee_scolaire, Bulletin, Classe, Cycle, Domain, Eleve, Emploi_du_temps, Enseignant, Evaluation, Matiere, Note, Parent, Semestre

# Register your models here.
@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'matricule', 'status')
    list_filter = ('status', 'classes')
    search_fields = ('prenom', 'nom', 'matricule', 'classes')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('nom_pere', 'nom_mere')
    search_fields = ('nom_pere', 'nom_mere')

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'matricule', 'specialite')
    list_filter = ('type_poste', 'classes')
    search_fields = ('prenom', 'nom', 'matricule')

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'coefficient', 'domain')
    list_filter = ('domain', 'classes')
    search_fields = ('nom',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'matiere', 'note', 'date', 'semestre')
    list_filter = ('matiere', 'semestre')
    search_fields = ('eleve__prenom', 'eleve__nom', 'matiere__nom')

@admin.register(Emploi_du_temps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('jour', 'heure_debut', 'heure_fin', 'classe', 'matiere', 'enseignant', 'date')
    list_filter = ('jour', 'classe', 'enseignant', 'date', 'classe')
    search_fields = ('classe__nom', 'matiere__nom', 'enseignant__prenom', 'enseignant__nom', 'classe')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('classe', 'matiere', 'type_d_evaluation', 'note', 'semestre')
    list_filter = ('matiere', 'type_d_evaluation', 'semestre')
    search_fields = ('matiere__nom',)

@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'annee_scolaire', 'notes')
    list_filter = ('eleve', 'annee_scolaire')
    search_fields = ('eleve__prenom', 'eleve__nom')

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'durée')
    search_fields = ('nom',)

@admin.register(Annee_scolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ('debut_annee', 'fin_annee')
    search_fields = ('debut_annee', 'fin_annee')

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee_scolaire',)
    search_fields = ('nom', 'annee_scolaire__debut_annee', 'cycle__nom')

@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('eleves', 'date', 'motif', 'duree')
    list_filter = ('date',)
    search_fields = ('eleves__prenom', 'eleves__nom', 'motif')