from django.db import models


class Reservation(models.Model):

    TYPE_CHOICES = [
        ("formation", "🎓 Formation"),
        ("site_web", "🌐 Création de site web"),
        ("application", "💻 Application / solution numérique"),
        ("communication", "📣 Communication digitale"),
        ("print", "🖨️ Impression"),
        ("media", "🎥 Média / couverture événementielle"),
        ("projet", "💼 Projet"),
        ("collaboration", "🤝 Collaboration"),
        ("partenariat", "🤝 Partenariat"),
        ("autre", "📩 Autre demande"),
    ]

    STATUS_CHOICES = [
        ("en_attente", "🟠 Nouvelle / En attente"),
        ("a_traiter", "🔵 À traiter"),
        ("contacte", "🟣 Contact effectué"),
        ("confirmee", "🟢 Confirmée"),
        ("en_cours", "🔷 En cours"),
        ("terminee", "✅ Terminée"),
        ("annulee", "🔴 Annulée"),
    ]

    PRIORITY_CHOICES = [
        ("basse", "🟢 Basse"),
        ("normale", "🔵 Normale"),
        ("haute", "🟠 Haute"),
        ("urgente", "🔴 Urgente"),
    ]

    MODE_CHOICES = [
        ("presentiel", "Présentiel"),
        ("en_ligne", "En ligne"),
    ]

    DUREE_CHOICES = [
        ("1_jour", "1 jour"),
        ("1_semaine", "1 semaine"),
        ("2_semaines", "2 semaines"),
        ("1_mois", "1 mois"),
        ("autre", "Autre durée"),
    ]

    # --------------------------------------------------------
    # IDENTITÉ DU DEMANDEUR
    # --------------------------------------------------------

    nom = models.CharField(
        max_length=150,
        verbose_name="Nom / entreprise"
    )

    telephone = models.CharField(
        max_length=30,
        verbose_name="Téléphone"
    )

    email = models.EmailField(
        verbose_name="Adresse e-mail"
    )

    organisation = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Organisation / entreprise"
    )

    # --------------------------------------------------------
    # DEMANDE
    # --------------------------------------------------------

    type_demande = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        verbose_name="Catégorie"
    )

    formation = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Formation / prestation"
    )

    date_souhaitee = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date souhaitée"
    )

    duree = models.CharField(
        max_length=30,
        choices=DUREE_CHOICES,
        blank=True,
        verbose_name="Durée"
    )

    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES,
        blank=True,
        verbose_name="Mode"
    )

    nombre_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Nombre de participants"
    )

    type_partenariat = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Type de partenariat"
    )

    budget = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Budget"
    )

    message = models.TextField(
        blank=True,
        verbose_name="Message / besoin exprimé"
    )

    # --------------------------------------------------------
    # SUIVI MDT
    # --------------------------------------------------------

    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="en_attente",
        verbose_name="Statut"
    )

    priorite = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normale",
        verbose_name="Priorité"
    )

    notes_internes = models.TextField(
        blank=True,
        verbose_name="Notes internes"
    )

    reponse_modele = models.ForeignKey(
        "ReponseAutomatique",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demandes",
        verbose_name="Modèle de réponse"
    )

    reponse_envoyee = models.BooleanField(
        default=False,
        verbose_name="Réponse envoyée"
    )

    date_reponse = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de réponse"
    )

    # --------------------------------------------------------
    # HISTORIQUE
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Demande reçue le"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Demande MDT"
        verbose_name_plural = "Demandes MDT"

    def __str__(self):
        return f"{self.nom} — {self.get_type_demande_display()}"

    @property
    def est_ouverte(self):
        return self.statut not in ["terminee", "annulee"]

class ReponseAutomatique(models.Model):
    TYPE_CHOICES = [
        ("contact", "Contact"),
        ("reservation", "Réservation"),
        ("projet", "Projet"),
        ("collaboration", "Collaboration"),
        ("partenariat", "Partenariat"),
        ("devis", "Demande de devis"),
        ("formation", "Formation"),
        ("information", "Demande d'information"),
    ]

    nom = models.CharField(
        max_length=150,
        verbose_name="Nom du modèle"
    )

    type_reponse = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )

    objet = models.CharField(
        max_length=255,
        verbose_name="Objet de l'e-mail"
    )

    message = models.TextField(
        verbose_name="Message"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Réponse active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["type_reponse", "nom"]
        verbose_name = "Réponse automatique"
        verbose_name_plural = "Réponses automatiques"

    def __str__(self):
        return f"{self.nom} — {self.get_type_reponse_display()}"
