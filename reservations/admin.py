from django.contrib import admin
from django.db.models import Q
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html, format_html_join
from django.utils.http import urlencode

from .models import Reservation


# ============================================================
# ACTIONS RAPIDES
# ============================================================

@admin.action(description="🟢 Confirmer les demandes sélectionnées")
def confirmer_demandes(modeladmin, request, queryset):
    queryset.update(statut="confirmee")


@admin.action(description="🔵 Marquer comme à traiter")
def traiter_demandes(modeladmin, request, queryset):
    queryset.update(statut="a_traiter")


@admin.action(description="🟣 Marquer comme contact effectué")
def marquer_contact(modeladmin, request, queryset):
    queryset.update(statut="contacte")


@admin.action(description="🔷 Marquer comme en cours")
def mettre_en_cours(modeladmin, request, queryset):
    queryset.update(statut="en_cours")


@admin.action(description="✅ Marquer comme terminées")
def terminer_demandes(modeladmin, request, queryset):
    queryset.update(statut="terminee")


@admin.action(description="✉️ Marquer la réponse comme envoyée")
def marquer_reponse_envoyee(modeladmin, request, queryset):
    queryset.update(
        reponse_envoyee=True,
        date_reponse=timezone.now()
    )


@admin.action(description="🔴 Marquer comme annulées")
def annuler_demandes(modeladmin, request, queryset):
    queryset.update(statut="annulee")


@admin.action(description="🟠 Priorité haute")
def priorite_haute(modeladmin, request, queryset):
    queryset.update(priorite="haute")


# ============================================================
# ADMIN
# ============================================================

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    change_list_template = (
        "admin/reservations/reservation/change_list.html"
    )

    list_display = (
        "demandeur_admin",
        "categorie_admin",
        "objet_admin",
        "priorite_admin",
        "statut_admin",
        "reponse_admin",
        "date_demande_admin",
        "actions_contact_admin",
    )

    list_filter = (
        "type_demande",
        "statut",
        "priorite",
        "reponse_envoyee",
        "mode",
        "created_at",
    )

    search_fields = (
        "nom",
        "telephone",
        "email",
        "organisation",
        "formation",
        "message",
        "notes_internes",
        "type_partenariat",
    )

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    list_per_page = 25

    readonly_fields = (
        "created_at",
        "updated_at",
        "date_reponse",
        "contact_buttons",
    )

    fieldsets = (

        (
            "👤 DEMANDEUR",
            {
                "fields": (
                    "nom",
                    "organisation",
                    "telephone",
                    "email",
                )
            },
        ),

        (
            "📋 DEMANDE",
            {
                "fields": (
                    "type_demande",
                    "formation",
                    "message",
                    "date_souhaitee",
                    "duree",
                    "mode",
                    "nombre_participants",
                    "type_partenariat",
                    "budget",
                )
            },
        ),

        (
            "📊 SUIVI MDT",
            {
                "fields": (
                    "statut",
                    "priorite",
                    "reponse_modele",
                    "reponse_envoyee",
                    "date_reponse",
                    "notes_internes",
                )
            },
        ),

        (
            "📞 CONTACTER",
            {
                "fields": (
                    "contact_buttons",
                )
            },
        ),

        (
            "🕒 HISTORIQUE",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    actions = (
        traiter_demandes,
        marquer_contact,
        confirmer_demandes,
        mettre_en_cours,
        terminer_demandes,
        marquer_reponse_envoyee,
        priorite_haute,
        annuler_demandes,
    )

    # ========================================================
    # AFFICHAGE LISTE
    # ========================================================

    @admin.display(description="Demandeur", ordering="nom")
    def demandeur_admin(self, obj):
        return format_html(
            '<div style="line-height:1.35;">'
            '<strong style="font-size:14px;">{}</strong><br>'
            '<span style="color:#64748b;font-size:12px;">{}</span>'
            '</div>',
            obj.nom,
            obj.email,
        )

    @admin.display(description="Catégorie", ordering="type_demande")
    def categorie_admin(self, obj):
        return obj.get_type_demande_display()

    @admin.display(description="Objet")
    def objet_admin(self, obj):
        if obj.formation:
            return obj.formation

        if obj.type_partenariat:
            return obj.type_partenariat

        if obj.message:
            texte = obj.message.replace("\n", " ")
            return texte[:60] + ("..." if len(texte) > 60 else "")

        return "—"

    @admin.display(description="Priorité", ordering="priorite")
    def priorite_admin(self, obj):

        couleurs = {
            "basse": "#16a34a",
            "normale": "#2563eb",
            "haute": "#ea580c",
            "urgente": "#dc2626",
        }

        couleur = couleurs.get(obj.priorite, "#64748b")

        return format_html(
            '<span style="display:inline-block;'
            'padding:4px 9px;border-radius:999px;'
            'background:{}15;color:{};font-weight:700;'
            'font-size:12px;">{}</span>',
            couleur,
            couleur,
            obj.get_priorite_display(),
        )

    @admin.display(description="Statut", ordering="statut")
    def statut_admin(self, obj):

        couleurs = {
            "en_attente": "#d97706",
            "a_traiter": "#2563eb",
            "contacte": "#7c3aed",
            "confirmee": "#16a34a",
            "en_cours": "#0891b2",
            "terminee": "#15803d",
            "annulee": "#dc2626",
        }

        couleur = couleurs.get(obj.statut, "#64748b")

        return format_html(
            '<span style="display:inline-block;'
            'padding:5px 10px;border-radius:999px;'
            'background:{}15;color:{};font-weight:700;'
            'font-size:12px;">{}</span>',
            couleur,
            couleur,
            obj.get_statut_display(),
        )

    @admin.display(description="Réponse")
    def reponse_admin(self, obj):

        if obj.reponse_envoyee:
            return format_html('<span style="color:#15803d;font-weight:700;">{}</span>', '✓ Envoyée')

        return format_html('<span style="color:#d97706;font-weight:700;">{}</span>', '○ À envoyer')

    @admin.display(description="Reçue le")
    def date_demande_admin(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M")

    @admin.display(description="Actions")
    def actions_contact_admin(self, obj):

        gmail_url = (
            "https://mail.google.com/mail/?view=cm&fs=1&to="
            + urlencode({"": obj.email})[1:]
        )

        outlook_url = (
            "https://outlook.live.com/mail/0/deeplink/compose?"
            + urlencode({"to": obj.email})
        )

        return format_html(
            '<div style="display:flex;gap:5px;flex-wrap:wrap;">'
            '<a href="{}" target="_blank" '
            'style="padding:5px 8px;border-radius:5px;'
            'background:#1d4ed8;color:white;text-decoration:none;'
            'font-size:11px;font-weight:700;">Gmail</a>'
            '<a href="{}" target="_blank" '
            'style="padding:5px 8px;border-radius:5px;'
            'background:#475569;color:white;text-decoration:none;'
            'font-size:11px;font-weight:700;">Outlook</a>'
            '<a href="mailto:{}" '
            'style="padding:5px 8px;border-radius:5px;'
            'background:#0f766e;color:white;text-decoration:none;'
            'font-size:11px;font-weight:700;">✉</a>'
            '<a href="tel:{}" '
            'style="padding:5px 8px;border-radius:5px;'
            'background:#0891b2;color:white;text-decoration:none;'
            'font-size:11px;font-weight:700;">☎</a>'
            '</div>',
            gmail_url,
            outlook_url,
            obj.email,
            obj.telephone,
        )

    @admin.display(description="Contacter le demandeur")
    def contact_buttons(self, obj):

        gmail_url = (
            "https://mail.google.com/mail/?view=cm&fs=1&"
            + urlencode({"to": obj.email})
        )

        outlook_url = (
            "https://outlook.live.com/mail/0/deeplink/compose?"
            + urlencode({"to": obj.email})
        )

        return format_html(
            '<div style="display:flex;gap:10px;flex-wrap:wrap;">'

            '<a href="{}" target="_blank" '
            'style="padding:10px 16px;background:#1d4ed8;'
            'color:#fff;border-radius:7px;text-decoration:none;'
            'font-weight:700;">'
            '✉️ Répondre avec Gmail'
            '</a>'

            '<a href="{}" target="_blank" '
            'style="padding:10px 16px;background:#475569;'
            'color:#fff;border-radius:7px;text-decoration:none;'
            'font-weight:700;">'
            '✉️ Répondre avec Outlook'
            '</a>'

            '<a href="mailto:{}" '
            'style="padding:10px 16px;background:#0f766e;'
            'color:#fff;border-radius:7px;text-decoration:none;'
            'font-weight:700;">'
            '✉️ E-mail'
            '</a>'

            '<a href="tel:{}" '
            'style="padding:10px 16px;background:#0891b2;'
            'color:#fff;border-radius:7px;text-decoration:none;'
            'font-weight:700;">'
            '☎️ Appeler'
            '</a>'

            '</div>',
            gmail_url,
            outlook_url,
            obj.email,
            obj.telephone,
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def changelist_view(self, request, extra_context=None):

        qs = self.get_queryset(request)

        context = {
            "total_demandes": qs.count(),
            "nouvelles": qs.filter(
                statut="en_attente"
            ).count(),
            "a_traiter": qs.filter(
                statut="a_traiter"
            ).count(),
            "contactes": qs.filter(
                statut="contacte"
            ).count(),
            "confirmees": qs.filter(
                statut="confirmee"
            ).count(),
            "en_cours": qs.filter(
                statut="en_cours"
            ).count(),
            "terminees": qs.filter(
                statut="terminee"
            ).count(),
            "urgentes": qs.filter(
                priorite="urgente"
            ).count(),
            "reponses_a_envoyer": qs.filter(
                reponse_envoyee=False
            ).exclude(
                statut="terminee"
            ).exclude(
                statut="annulee"
            ).count(),
        }

        if extra_context:
            context.update(extra_context)

        return super().changelist_view(
            request,
            extra_context=context
        )

from .models import ReponseAutomatique

@admin.register(ReponseAutomatique)
class ReponseAutomatiqueAdmin(admin.ModelAdmin):
    list_display = ("nom", "type_reponse", "objet", "active", "updated_at")
    list_filter = ("type_reponse", "active")
    search_fields = ("nom", "objet", "message")
    list_editable = ("active",)


# ============================================================
# RÉPONSES MDT
# ============================================================

from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone

from .models import Reservation, ReponseAutomatique


def envoyer_reponse_mdt(modeladmin, request, queryset):
    envoyees = 0

    for reservation in queryset:
        reponse = reservation.reponse_modele

        if not reponse:
            continue

        if not reponse.active:
            continue

        if not reservation.email:
            continue

        message = reponse.message.replace(
            "{{nom}}",
            reservation.nom
        )

        message = message.replace(
            "{{formation}}",
            reservation.formation or ""
        )

        message = message.replace(
            "{{type_demande}}",
            reservation.get_type_demande_display()
        )

        send_mail(
            reponse.objet,
            message,
            "contact.missdigital@gmail.com",
            [reservation.email],
            fail_silently=False,
        )

        reservation.reponse_envoyee = True
        reservation.date_reponse = timezone.now()
        reservation.save(
            update_fields=["reponse_envoyee", "date_reponse"]
        )

        envoyees += 1

    if envoyees:
        messages.success(
            request,
            f"{envoyees} réponse(s) envoyée(s) avec succès."
        )
    else:
        messages.warning(
            request,
            "Aucune réponse envoyée. Vérifie qu'un modèle actif est sélectionné."
        )


envoyer_reponse_mdt.short_description = "✉️ Envoyer la réponse sélectionnée"


if not any(
    getattr(item, "model", None) is Reservation
    for item in admin.site._registry.values()
):

    @admin.register(Reservation)
    class ReservationAdminMDT(admin.ModelAdmin):
        list_display = (
            "nom",
            "email",
            "type_demande",
            "statut",
            "reponse_modele",
            "reponse_envoyee",
            "date_reponse",
        )

        list_filter = (
            "type_demande",
            "statut",
            "reponse_envoyee",
        )

        search_fields = (
            "nom",
            "email",
            "telephone",
            "message",
        )

        actions = [envoyer_reponse_mdt]

        fieldsets = (
            ("Informations client", {
                "fields": (
                    "nom",
                    "email",
                    "telephone",
                )
            }),
            ("Demande", {
                "fields": (
                    "type_demande",
                    "message",
                    "formation",
                    "date_souhaitee",
                    "duree",
                    "mode",
                )
            }),
            ("Suivi MDT", {
                "fields": (
                    "statut",
                    "notes_internes",
                    "reponse_modele",
                    "reponse_envoyee",
                    "date_reponse",
                )
            }),
        )

        readonly_fields = (
            "reponse_envoyee",
            "date_reponse",
        )


# ============================================================
# ENVOI RÉEL DES RÉPONSES AUTOMATIQUES
# ============================================================

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from .models import ReponseAutomatique


TYPE_REPONSE_PAR_DEFAUT = {
    "formation": "formation",
    "site_web": "devis",
    "application": "devis",
    "communication": "devis",
    "print": "devis",
    "media": "devis",
    "projet": "projet",
    "collaboration": "collaboration",
    "partenariat": "partenariat",
    "autre": "information",
}


@admin.action(description="✉️ Envoyer la réponse automatique")
def envoyer_reponse_automatique(modeladmin, request, queryset):

    envoyees = 0
    ignorees = 0

    for reservation in queryset:

        if reservation.reponse_envoyee:
            ignorees += 1
            continue

        if not reservation.email:
            ignorees += 1
            continue

        reponse = reservation.reponse_modele

        if not reponse or not reponse.active:
            type_reponse = TYPE_REPONSE_PAR_DEFAUT.get(
                reservation.type_demande,
                "information"
            )

            reponse = ReponseAutomatique.objects.filter(
                type_reponse=type_reponse,
                active=True
            ).order_by("id").first()

        if not reponse:
            ignorees += 1
            continue

        variables = {
            "{{nom}}": reservation.nom or "",
            "{{email}}": reservation.email or "",
            "{{telephone}}": reservation.telephone or "",
            "{{formation}}": reservation.formation or "",
            "{{type_demande}}": reservation.get_type_demande_display(),
            "{{organisation}}": getattr(reservation, "organisation", "") or "",
            "{{budget}}": getattr(reservation, "budget", "") or "",
        }

        objet = reponse.objet
        message_mail = reponse.message

        for variable, valeur in variables.items():
            objet = objet.replace(variable, str(valeur))
            message_mail = message_mail.replace(variable, str(valeur))

        send_mail(
            subject=objet,
            message=message_mail,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.email],
            fail_silently=False,
        )

        reservation.reponse_modele = reponse
        reservation.reponse_envoyee = True
        reservation.date_reponse = timezone.now()
        reservation.save()

        envoyees += 1

    if envoyees:
        messages.success(
            request,
            f"{envoyees} réponse(s) automatique(s) envoyée(s) avec succès."
        )

    if ignorees:
        messages.warning(
            request,
            f"{ignorees} demande(s) ignorée(s) : déjà envoyée(s), e-mail absent ou modèle indisponible."
        )


# Ajout de l'action au ReservationAdmin EXISTANT
actions_actuelles = list(getattr(ReservationAdmin, "actions", []) or [])

if envoyer_reponse_automatique not in actions_actuelles:
    actions_actuelles.append(envoyer_reponse_automatique)
    ReservationAdmin.actions = actions_actuelles
