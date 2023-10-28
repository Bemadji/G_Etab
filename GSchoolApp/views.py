from pyexpat.errors import messages
from tarfile import RECORDSIZE
from django.shortcuts import get_object_or_404, redirect, render
from GSchoolApp.models import *
from django.contrib.auth import authenticate, login, logout
from G_School.forms import ContactForm, InscriptionForm, LoginForm, NoteForm, SignUpForm


def accueil(request):
    return render(request, "index.html")


# === Vue pour afficher la liste des élèves ========================================================================================================================
def liste_eleves(request):
    # Triez les élèves par le champ 'classes'
    eleves = Eleve.objects.all().order_by('classes')
    return render(request, 'liste/liste_eleves.html', {'eleves': eleves})

# === Vue pour afficher les détails d'un élève =====================================================================================================================
def detail_eleve(request, eleve_id):
    eleve = get_object_or_404(Eleve, pk=eleve_id)
    return render(request, 'details/detail_eleve.html', {'eleve': eleve})


# === Vue pour afficher la liste des enseignants ====================================================================================================================
def liste_enseignant(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'liste/liste_enseignant.html', {'enseignants': enseignants})


# === Vue pour afficher les détails d'un enseignant =================================================================================================================
def detail_enseignant(request, id):
    enseignant = get_object_or_404(Enseignant, id=id)
    return render(request, 'details/detail_enseignant.html', {'enseignant': enseignant})

# === Vue pour afficher la liste des classes ========================================================================================================================
def liste_classes(request):
    classes = Classe.objects.all()
    return render(request, 'liste/liste_classes.html', {'classes': classes})


# ==== Vue pour afficher les détails d'une classe ==================================================================================================================
def detail_classe(request, classe_id):
    classe = get_object_or_404(Classe, pk=classe_id)
    # On compte le nombre d'élèves dans la classe
    nombre_eleves = Classe.objects.filter(eleves__isnull=False).filter(eleves__classe=classe).count()
    return render(request, 'detail_classe.html', {'classe': classe, 'nombre_eleves': nombre_eleves,})


# === Vue pour afficher la liste des matières =====================================================================================================================
def liste_matieres(request):
    matieres = Matiere.objects.all()
    return render(request, 'liste/liste_matieres.html', {'matieres': matieres})


# ====== Vue pour afficher les détails d'une matière ============================================================================================================== 
def detail_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, pk=matiere_id)
    return render(request, 'details/detail_matiere.html', {'matiere': matiere})


# === Vue pour afficher la liste des notes d'un élève ============================================================================================================
def liste_notes_eleve(request, eleve_id):
    eleve = get_object_or_404(Eleve, pk=eleve_id)
    notes = eleve.note_set.all()  # Accéder aux notes de l'élève via la relation inverse
    return render(request, 'base.html', {'eleve': eleve, 'notes': notes})


def liste_notes(request):
    notes = Note.objects.all()
    return render(request, 'liste/liste_notes_eleve.html', {'notes': notes})


# === Vue pour afficher la liste des notes pour une matière donnée ===============================================================================
def liste_notes_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, pk=matiere_id)
    notes = Note.objects.filter(matiere=matiere)
    return render(request, 'liste/liste_notes_matiere.html', {'matiere': matiere, 'notes': notes})

# ==== Affichage des notes par classe ==============================================================================================================
def afficher_notes_par_classe(request, classe_id):
    classe = Classe.objects.get(id=classe_id)
    eleves = Eleve.objects.filter(classe=classe)
    notes = Note.objects.filter(eleve__in=eleves)
    context = {
        'classe': classe,
        'eleves': eleves,
        'notes': notes,
    }
    return render(request, 'afficher_notes_par_classe.html', context)

# === Ajout d'une note Views ===================================================================================================================================
def ajouter_note(request, eleve_id):
    eleve = Eleve.objects.get(id=eleve_id)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.eleve = eleve
            note.save()
            return redirect('afficher_notes_par_classe', classe_id=eleve.classe.id)
    else:
        form = NoteForm()

    context = {
        'eleve': eleve,
        'form': form,
    }
    return render(request, 'ajouter_note.html', context)

# === Vue pour afficher l'emploi du temps d'une classe ===============================================================================================
def emploi_du_temps(request):
    emplois = Emploi_du_temps.objects.all()
    return render(request, 'emploi_du_temps.html', {'emploi_du_temps': emplois})


# === Vue pour afficher la liste des évaluations =====================================================================================================
def liste_evaluations(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'liste/liste_evaluations.html', {'evaluations': evaluations})


# === Vue pour afficher les détails d'une évaluation =================================================================================================
def detail_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    return render(request, 'details/detail_evaluation.html', {'evaluation': evaluation})


# === Vue pour afficher le bulletin d'un élève =======================================================================================================
def bulletins_eleve(request, eleve_id):
    eleve = get_object_or_404(Eleve, pk=eleve_id)
    bulletins = Bulletin.objects.filter(eleve=eleve)
    return render(request, 'bulletin_eleve.html', {'eleve': eleve, 'bulletins': bulletins})


# === Vue pour afficher les détails d'un bulletin ====================================================================================================
def detail_bulletin(request, bulletin_id):
    bulletin = get_object_or_404(Bulletin, pk=bulletin_id)
    matieres = bulletin.matiere_set.all()  # Supposons que vous ayez un champ "matiere_set" dans le modèle Bulletin
    return render(request, 'details/detail_bulletin.html', {'bulletin': bulletin, 'matieres': matieres})


# ======= Vue pour afficher la liste des années scolaires ============================================================================================
def liste_annees_scolaires(request):
    annees_scolaires = Annee_scolaire.objects.all()
    return render(request, 'liste/liste_annees_scolaires.html', {'annees_scolaires': annees_scolaires})


# ====== Vue pour afficher les détails d'une année scolaire ==========================================================================================
def detail_annee_scolaire(request, annee_scolaire_id):
    annee_scolaire = get_object_or_404(Annee_scolaire, pk=annee_scolaire_id)
    return render(request, 'details/detail_annee_scolaire.html', {'annee_scolaire': annee_scolaire})


# ==== Vue pour afficher la liste des semestres d'une année scolaire donnée ===========================================================================
def liste_semestres_annee_scolaire(request, annee_scolaire_id):
    annee_scolaire = get_object_or_404(Annee_scolaire, pk=annee_scolaire_id)
    semestres = Semestre.objects.filter(annee_scolaire=annee_scolaire)
    return render(request, 'liste/liste_semestres_annee_scolaire.html', {'annee_scolaire': annee_scolaire, 'semestres': semestres})


# ===== Vue pour afficher les détails d'un semestre ====================================================================================================
def detail_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, pk=semestre_id)
    return render(request, 'detail_semestre.html', {'semestre': semestre})


# ===== Vue pour afficher la liste des absences d'un élève ============================================================================
def liste_absences(request, eleve_id):
    eleve = get_object_or_404(Eleve, pk=eleve_id)
    absences = Absence.objects.filter(eleves=eleve)
    return render(request, 'liste/liste_absences.html', {'eleve': eleve, 'absences': absences})

# ===== Contacte views =================================================================================================================
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            # Save the form data to the database.
            pass
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


# === Vue pour la liste des classes ====================================================================================================
def liste_classes(request):
    classes = Classe.objects.all()
    classe_eleves = {}
    
    for classe in classes:
        eleves = classe.eleve_set.all()  # Utilisez le nom de la relation inverse, qui est automatiquement généré par Django
        classe_eleves[classe] = eleves
    
    return render(request, 'liste/liste_classes.html', {'classes': classes, 'classe_eleves': classe_eleves})

# ==== Détail classe views ==============================================================================================================
def detail_classe(request, classe_id):
    classe = get_object_or_404(Classe, pk=classe_id)
    return render(request, 'details/detail_classe.html', {'classe': classe})

def about_page(request):
    return render(request, 'about.html')


# ==== Authentification =================================================================================================================
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Vous êtes maintenant connecté.")
                return redirect('dashboard')  # Rediriger vers la page d'accueil après la connexion réussie
            else:
                messages.error(request, 'La connexion a échoué. Veuillez vérifier vos identifiants.')
                # Gérer le cas d'une connexion échouée
                return render(request, 'authen/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'authen/login.html', {'form': form})

# == Register Views =========================================================================================================================
def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Votre inscription a réussi. Vous pouvez maintenant vous connecter.')
            # Authentifiez l'utilisateur après l'inscription
            login(request, user)
            return redirect('login') 
    else:
        form = SignUpForm()
    return render(request, 'authen/register_view.html', {"form": form})


# ==== Logout Views ==========================================================================================================================
def user_logout(request):
    logout(request)
    return redirect('login')

# == Inscription views ========================================================================================================================
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_eleves')  # Redirigez l'utilisateur vers une page d'accueil ou une autre page après l'inscription réussie
    else:
        form = InscriptionForm()

    return render(request, 'inscription.html', {'form': form})

# === Page not found 404 Views ================================================================================================================
def handle_not_found(request, exception):
    return render(request, '4O4.html' )