from django.core.mail import send_mail
from django.shortcuts import render

from reservations.forms import ReservationForm
from reservations.models import Reservation


MDT_EMAIL = "contact.missdigital@gmail.com"


def get_reponse_automatique(type_reponse):
    from reservations.models import ReponseAutomatique

    return ReponseAutomatique.objects.filter(
        type_reponse=type_reponse,
        active=True
    ).first()


def home(request):
    return render(request, "website/home.html")


def tech(request):
    return render(request, "website/pages/tech.html")


def com(request):
    return render(request, "website/pages/com.html")


def print_services(request):
    return render(request, "website/pages/print.html")


def media(request):
    return render(request, "website/pages/media.html")


def academy(request):
    return render(request, "website/pages/academy.html")


def portfolio(request):
    return render(request, "website/pages/portfolio.html")


def founder(request):
    return render(request, "website/pages/founder.html")


def show(request):
    return render(request, "website/pages/show.html")


def equip(request):
    return render(request, "website/pages/equip.html")


def contact(request):

    if request.method == "POST":

        nom = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        telephone = request.POST.get("phone", "").strip()
        type_demande = request.POST.get("type", "").strip()
        message = request.POST.get("message", "").strip()

        type_mapping = {
            "projet": "projet",
            "collaboration": "partenariat",
            "partenariat": "partenariat",
            "autre": "autre",
        }

        reservation = Reservation.objects.create(
            nom=nom,
            email=email,
            telephone=telephone,
            type_demande=type_mapping.get(
                type_demande,
                "autre"
            ),
            message=message,
        )

        type_label = dict(
            Reservation.TYPE_CHOICES
        ).get(
            reservation.type_demande,
            "Demande"
        )

        # ----------------------------------------------------
        # EMAIL À SALY / MISS DIGITAL TECH
        # ----------------------------------------------------

        subject = f"Nouvelle demande MDT — {type_label}"

        body = f"""
Bonjour Saly,

Une nouvelle demande vient d'être reçue sur le site
Miss Digital Tech.

----------------------------------------
NOUVELLE DEMANDE
----------------------------------------

Nom : {nom}
E-mail : {email}
Téléphone : {telephone or "Non renseigné"}
Type : {type_label}

Message :
{message}

----------------------------------------

Cette demande est également disponible
dans Django Admin.

Miss Digital Tech
L'innovation au service de votre réussite.
"""

        try:
            send_mail(
                subject,
                body,
                MDT_EMAIL,
                [MDT_EMAIL],
                fail_silently=False,
            )

            # ------------------------------------------------
            # CONFIRMATION AU CLIENT
            # ------------------------------------------------

            reponse = get_reponse_automatique("contact")

            if reponse:
                client_subject = reponse.objet
                client_body = reponse.message.replace("{{nom}}", nom)
            else:
                client_subject = "Votre demande a bien été reçue — Miss Digital Tech"
                client_body = f"""
Bonjour {nom},

Nous avons bien reçu votre demande concernant :

{type_label}

Merci d'avoir contacté Miss Digital Tech.

Notre équipe reviendra vers vous prochainement.

Bien cordialement,

Miss Digital Tech
Dakar, Sénégal

L'innovation au service de votre réussite.
"""

            send_mail(
                client_subject,
                client_body,
                MDT_EMAIL,
                [email],
                fail_silently=False,
            )

        except Exception:
            # La demande reste enregistrée dans Django Admin
            pass

        return render(
            request,
            "website/pages/contact.html",
            {
                "success": True,
            }
        )

    return render(
        request,
        "website/pages/contact.html"
    )


def reservation(request):

    success = False

    if request.method == "POST":

        form = ReservationForm(request.POST)

        if form.is_valid():

            reservation_obj = form.save()

            # ------------------------------------------------
            # EMAIL À SALY
            # ------------------------------------------------

            subject = (
                "Nouvelle réservation de formation — MDT Academy"
            )

            body = f"""
Bonjour Saly,

Une nouvelle réservation de formation vient d'être
enregistrée sur le site Miss Digital Tech.

----------------------------------------
RÉSERVATION DE FORMATION
----------------------------------------

Nom : {reservation_obj.nom}
E-mail : {reservation_obj.email}
Téléphone : {reservation_obj.telephone}

Formation :
{reservation_obj.get_formation_display()
 if hasattr(reservation_obj, "get_formation_display")
 else reservation_obj.formation}

Date souhaitée : {reservation_obj.date_souhaitee}
Durée : {reservation_obj.get_duree_display()
 if reservation_obj.duree else "Non renseignée"}

Mode : {reservation_obj.get_mode_display()
 if reservation_obj.mode else "Non renseigné"}

Participants : {reservation_obj.nombre_participants or "Non renseigné"}

Message :
{reservation_obj.message or "Aucun message"}

----------------------------------------

Statut actuel : En attente

La réservation est disponible dans Django Admin.

Miss Digital Tech
MDT Academy
"""

            try:
                send_mail(
                    subject,
                    body,
                    MDT_EMAIL,
                    [MDT_EMAIL],
                    fail_silently=False,
                )

                # ------------------------------------------------
                # CONFIRMATION AU CLIENT
                # ------------------------------------------------

                reponse = get_reponse_automatique("reservation")

                if reponse:
                    client_subject = reponse.objet
                    client_body = reponse.message.replace(
                        "{{nom}}",
                        reservation_obj.nom
                    )
                else:
                    client_subject = (
                        "Votre demande de formation a bien été reçue — MDT Academy"
                    )

                    client_body = f"""
Bonjour {reservation_obj.nom},

Nous avons bien reçu votre demande de réservation.

Votre demande est actuellement en attente de confirmation.

Bien cordialement,

MDT Academy — Miss Digital
Dakar, Sénégal

L'innovation au service de votre réussite.
"""

                send_mail(
                    client_subject,
                    client_body,
                    MDT_EMAIL,
                    [reservation_obj.email],
                    fail_silently=False,
                )

            except Exception:
                pass

            success = True

        else:

            return render(
                request,
                "website/pages/reserver.html",
                {
                    "form": form,
                    "success": False,
                }
            )

    else:
        form = ReservationForm()

    return render(
        request,
        "website/pages/reserver.html",
        {
            "form": form,
            "success": success,
        }
    )
