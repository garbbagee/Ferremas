from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente

class ClienteForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'Correo electrónico'})
        self.fields['password1'].widget.attrs.update({'class': 'input', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'input', 'placeholder': 'Confirma tu contraseña'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

