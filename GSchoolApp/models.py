from itertools import count
from django.db import models
from django.db.models import Sum


# Create your models here.
class Classe(models.Model):
    nom = models.CharField(max_length=35, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom
    
    
class Personne(models.Model):
    Genre = (
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    )
    prenom = models.CharField('Prénom', max_length=150)
    nom = models.CharField('Nom', max_length=150)
    date_naissance = models.DateField('Date de naissance', max_length=150)
    lieu_naissance = models.TextField('Lieu de naissance', max_length=150)
    genre = models.CharField(max_length=1, choices=Genre)
    adresse = models.TextField('Adresse', max_length=150)
    phone_number = models.CharField('Numéro téléphone', max_length=10)
    email = models.EmailField('Adresse Email', max_length=50)
    photo = models.ImageField(upload_to="photo", blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    
class Eleve(Personne):
    Status = (
        ('Nouveau', 'Nouveau élève'),
        ('Ancien', 'Ancien élève'),
    )
    matricule = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=32, choices=Status)
    classes = models.ForeignKey(Classe, on_delete=models.CASCADE)  # Utilisez ForeignKey pour la classe
    date_inscription = models.DateField(default=True)
    
    @property
    def moyenne(self):
        """
        Calcule la moyenne des notes de l'élève.

        Returns:
            float: La moyenne des notes de l'élève.
        """

        notes = Note.objects.filter(eleve=self)
        somme_notes = notes.aggregate(somme=Sum('note'))['somme']
        nombre_notes = notes.count()

        if nombre_notes == 0:
            return 0.0

        moyenne = somme_notes / nombre_notes
        return moyenne

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def save(self, *args, **kwargs):
        # Générez un matricule unique en fonction de l'ID de l'objet
        if not self.matricule:
            self.matricule = f"ELE-{self.id}"
        super(Eleve, self).save(*args, **kwargs)


class Parent(models.Model):
    nom_pere = models.CharField('Nom du Père', max_length=150)
    nom_mere = models.CharField('Nom de la Mère', max_length=150)
    phone_number1 = models.CharField(max_length=10)
    phone_number2 = models.CharField(max_length=10)
    adresse = models.TextField(max_length=150)
    eleves = models.ManyToManyField(Eleve)

    
class Enseignant(Personne):
    Categorie = (
        ('Per', 'Permanent'),
        ('Vac', 'Vacataire'),
    )
    matricule = models.CharField(max_length=20, unique=True)
    poste = models.CharField(max_length=60)
    type_poste = models.CharField(max_length=60, choices=Categorie)
    diplome = models.CharField(max_length=60)
    specialite = models.CharField(max_length=70)
    classes = models.ManyToManyField('Classe')
    fonction = models.CharField(max_length=60, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Générez un matricule unique en fonction de l'ID de l'objet
        if not self.matricule:
            self.matricule = f"ENS-{self.id}"
        super(Enseignant, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.specialite})"
    
    
class Domain(models.Model):
    nom = models.CharField(max_length=32)

    def __str__(self):
        return self.nom
    
class Matiere(models.Model):
    nom = models.CharField(max_length=60, unique=True)
    description = models.TextField(max_length=180)
    coefficient = models.PositiveIntegerField()
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    classes = models.ManyToManyField('Classe')

    def __str__(self):
        return self.nom
    
class Note(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    note = models.FloatField(default=0.0)
    date = models.DateField()
    semestre = models.ForeignKey('Semestre', on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note de {self.eleve.prenom} {self.eleve.nom} en {self.matiere.nom} - Classe: {self.eleve.classes.nom}"
    
    
class Emploi_du_temps(models.Model):
    jour = models.CharField(max_length=60)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    date = models.DateField()
    
    # classer les enregistrements par classe en plus de les regrouper par jour
def group_by_day_and_class(self):
        return (
            Emploi_du_temps.objects
            .values('jour', 'classe__nom')  # Remarquez 'classe__nom' pour obtenir le nom de la classe
            .annotate(count=count('jour'))
            .order_by('jour', 'classe__nom')  # Remarquez 'classe__nom' ici aussi
        )



class Evaluation(models.Model):
    Type_eva = (
        ('Contrôle', 'Contrôle Continu'),
        ('Exam', 'Examen'),
    )
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    type_d_evaluation = models.CharField(max_length=55, choices=Type_eva)
    note = models.FloatField()
    semestre = models.ForeignKey('Semestre', on_delete=models.CASCADE)
    jour = models.DateTimeField()

class Bulletin(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    annee_scolaire = models.ForeignKey('Annee_scolaire', on_delete=models.CASCADE)
    matieres = models.ManyToManyField(Matiere)
    notes = models.FloatField(default=1.0)
    semestre = models.ForeignKey('Semestre', on_delete=models.CASCADE)


class Cycle(models.Model):
    nom = models.CharField(max_length=55, unique=True)
    durée = models.DateField()
    classes = models.ManyToManyField(Classe)

    def __str__(self):
        return self.nom
    

class Annee_scolaire(models.Model):
    debut_annee = models.DateField()
    fin_annee = models.DateField()
    cycles = models.ManyToManyField(Cycle)

class Semestre(models.Model):
    nom = models.CharField(max_length=55, unique=True)
    annee_scolaire = models.ForeignKey(Annee_scolaire, on_delete=models.CASCADE)
    cycles = models.ManyToManyField(Cycle)

    def __str__(self):
        return self.nom

class Absence(models.Model):
    eleves = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    date = models.DateField()
    motif = models.CharField(max_length=200)
    duree = models.DateTimeField()

    def __str__(self):
        return f"{self.eleves} ({self.date}): {self.motif}"