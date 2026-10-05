from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation

        fields = [
            "nom",
            "telephone",
            "email",
            "formation",
            "date_souhaitee",
            "duree",
            "mode",
            "nombre_participants",
            "message",
        ]

        widgets = {
            "nom": forms.TextInput(attrs={
                "placeholder": "Votre nom complet",
            }),

            "telephone": forms.TextInput(attrs={
                "placeholder": "+221 XX XXX XX XX",
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "votre@email.com",
            }),

            "formation": forms.Select(
                choices=[
                    ("", "Choisir une formation"),
                    ("developpement_web", "Développement Web"),
                    ("bureautique", "Bureautique"),
                    ("intelligence_artificielle", "Intelligence Artificielle"),
                    ("cybersecurite", "Cybersécurité"),
                    ("marketing_communication", "Marketing & Communication"),
                    ("autre", "Autre formation"),
                ]
            ),

            "date_souhaitee": forms.DateInput(attrs={
                "type": "date",
            }),

            "duree": forms.Select(),

            "mode": forms.Select(),

            "nombre_participants": forms.NumberInput(attrs={
                "placeholder": "Nombre de participants",
                "min": "1",
            }),

            "message": forms.Textarea(attrs={
                "placeholder": (
                    "Précisez votre niveau, vos objectifs "
                    "ou toute information utile..."
                ),
                "rows": 5,
            }),
        }

    def save(self, commit=True):
        reservation = super().save(commit=False)

        reservation.type_demande = "formation"

        if commit:
            reservation.save()

        return reservation


class DemandeMDTForm(forms.ModelForm):

    class Meta:
        model = Reservation

        fields = [
            "nom",
            "telephone",
            "email",
            "organisation",
            "date_souhaitee",
            "budget",
            "type_partenariat",
            "message",
        ]

        widgets = {
            "nom": forms.TextInput(attrs={
                "placeholder": "Votre nom complet",
            }),

            "telephone": forms.TextInput(attrs={
                "placeholder": "+221 XX XXX XX XX",
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "votre@email.com",
            }),

            "organisation": forms.TextInput(attrs={
                "placeholder": "Nom de votre entreprise / organisation",
            }),

            "date_souhaitee": forms.DateInput(attrs={
                "type": "date",
            }),

            "budget": forms.TextInput(attrs={
                "placeholder": "Budget indicatif (facultatif)",
            }),

            "type_partenariat": forms.TextInput(attrs={
                "placeholder": "Précisez le type de partenariat",
            }),

            "message": forms.Textarea(attrs={
                "placeholder": (
                    "Décrivez votre demande, votre projet "
                    "ou votre proposition..."
                ),
                "rows": 6,
            }),
        }