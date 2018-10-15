from django import forms


class ArticleRecommendForm(forms.Form):
    """Formulario para recomendar articulo."""
    name = forms.CharField(
        label='Nombre'
    )
    from_email = forms.EmailField(
        label='Tu email',
        widget=forms.EmailInput()
    )
    to_email = forms.EmailField(
        label='Email destinatario',
        widget=forms.EmailInput()
    )
    message = forms.CharField(
        label='Mensaje (Opcional)',
        required=False,
        widget=forms.Textarea()
    )
