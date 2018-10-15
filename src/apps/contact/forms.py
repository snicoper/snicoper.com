from django import forms


class ContactForm(forms.Form):
    """Formulario de contacto base."""

    subject = forms.CharField(
        label='Tema',
        max_length=255,
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput()
    )
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea()
    )
