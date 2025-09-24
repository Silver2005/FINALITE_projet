from django.db import models
from django.contrib.auth.models import User

# Modèle pour les articles
class Article(models.Model):
    code_article = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=255)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.code_article} - {self.designation}"

# Modèle pour les fournisseurs
class Fournisseur(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nom

# Modèle pour la Demande de Matériel
class DemandeDeMateriel(models.Model):
    TYPES_SERVICE = [
        ('chef_de_centre', 'Chef de centre'),
        ('service_distribution', 'Service distribution'),
        ('service_moyens_generaux', 'Service moyens généraux'),
        ('prestataire', 'Prestataire'),
    ]

    numero = models.CharField(max_length=20, blank=True, null=True)
    justification = models.TextField()
    nature_des_prestations = models.CharField(max_length=100, choices=TYPES_SERVICE)
    
    # Le bénéficiaire est lié directement à l'utilisateur connecté
    beneficiaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_beneficiaire')
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True)

    imputation = models.CharField(max_length=50)
    credit = models.CharField(max_length=50)
    
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Demande n° {self.numero} par {self.beneficiaire.username}"

# Modèle pour chaque ligne d'article dans la Demande de Matériel
class LigneDeCommande(models.Model):
    demande = models.ForeignKey(
        'DemandeDeMateriel',
        on_delete=models.CASCADE,
        related_name='lignes'
    )
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    quantite = models.PositiveIntegerField()

    def total_ligne(self):
        if self.article:
            return self.article.prix_unitaire * self.quantite
        return 0

    def __str__(self):
        if self.article:
            return f"{self.quantite} x {self.article.designation}"
        return f"Ligne sans article"