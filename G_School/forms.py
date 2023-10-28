from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from GSchoolApp.models import Eleve, Note, Parent, Personne

#from .models import Record

class AuthenticationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'id': 'loginName'}),
        label="Email address or username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'loginPassword'}),
        label="Password"
    )


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requis. 30 caractères ou moins.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requis. 30 caractères ou moins.')
    email = forms.EmailField(max_length=254, required=True, help_text='Requis. Entrez une adresse e-mail valide.')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['prenom', 'nom', 'date_naissance', 'lieu_naissance', 'genre', 'adresse', 'phone_number', 'email', 'photo']
        
class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['prenom', 'nom', 'date_naissance', 'lieu_naissance', 'genre', 'adresse', 'phone_number', 'email', 'photo', 'matricule', 'status', 'classes']
                
class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['nom_pere', 'nom_mere', 'phone_number1', 'phone_number2', 'adresse']



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['matiere', 'note', 'date', 'semestre']
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=55, label="Votre nom")
    email = forms.EmailField(label="Votre adresse e-mail")
    subject = forms.CharField(max_length=255, label="Sujet")
    message = forms.CharField(widget=forms.Textarea, label="Message")
