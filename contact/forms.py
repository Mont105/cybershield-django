import re

from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator

# opciones del servicio requerido
SERVICE_CHOICES = [
    ('', 'Seleccione un servicio...'),
    ('ofensivo', 'Test de Intrusión / Red Team'),
    ('defensivo', 'Monitoreo SOC y SIEM'),
    ('infraestructura', 'Hardening de Servidores / Cloud'),
    ('forense', 'Análisis Forense / DFIR'),
    ('normativa', 'Auditoría ISO 27001'),
    ('otro', 'Otro Requerimiento TI'),
]

# dominios de correo no corporativos
FREE_EMAIL_DOMAINS = {'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'live.com'}

# validadores de nombre y teléfono
name_validator = RegexValidator(
    regex=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]+$",
    message="El nombre solo puede contener letras y espacios.",
)
phone_validator = RegexValidator(
    regex=r"^\+?56\s?9\s?\d{4}\s?\d{4}$",
    message="Ingrese un celular chileno válido. Ej: +56 9 1234 5678",
)


# formulario de contacto
class ContactForm(forms.Form):
    # campos del formulario
    name = forms.CharField(
        label="Nombre y Apellido",
        max_length=80,
        validators=[MinLengthValidator(3), name_validator],
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Roberto Fuentes'}),
    )
    email = forms.EmailField(
        label="Correo Corporativo",
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'rfuentes@empresa.com'}),
    )
    phone = forms.CharField(
        label="Teléfono (opcional)",
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+56 9 1234 5678'}),
    )
    company = forms.CharField(
        label="Empresa",
        max_length=100,
        validators=[MinLengthValidator(2)],
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Empresa SpA'}),
    )
    service_type = forms.ChoiceField(
        label="Servicio Requerido",
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    message = forms.CharField(
        label="Detalle del Requerimiento",
        validators=[MinLengthValidator(20), MaxLengthValidator(1000)],
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Describa el alcance...'}),
    )
    accept_terms = forms.BooleanField(
        label="Acepto que CyberShield me contacte para responder esta solicitud",
        error_messages={'required': "Debe aceptar para enviar la solicitud."},
    )

    # validaciones personalizadas por campo
    def clean_name(self):
        name = " ".join(self.cleaned_data['name'].split())
        if len(name.split(" ")) < 2:
            raise forms.ValidationError("Ingrese nombre y apellido.")
        return name.title()

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        domain = email.rsplit('@', 1)[-1]
        if domain in FREE_EMAIL_DOMAINS:
            raise forms.ValidationError("Utilice un correo corporativo (no Gmail, Hotmail, Outlook, etc.).")
        return email

    def clean_phone(self):
        return re.sub(r"\s+", "", self.cleaned_data['phone'])

    # validación cruzada entre servicio y mensaje
    def clean(self):
        cleaned = super().clean()
        if cleaned.get('service_type') == 'otro' and len(cleaned.get('message', '')) < 50:
            self.add_error('message', "Para 'Otro Requerimiento' describa el alcance con al menos 50 caracteres.")
        return cleaned
