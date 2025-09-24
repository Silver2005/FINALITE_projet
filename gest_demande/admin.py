from django.contrib import admin
from .models import Fournisseur, DemandeDeMateriel, LigneDeCommande, Article
# L'import de Beneficiaire a été supprimé

class LigneDeCommandeInline(admin.TabularInline):
    model = LigneDeCommande
    extra = 1  # Permet d'ajouter 1 ligne de commande vide par défaut

@admin.register(DemandeDeMateriel)
class DemandeDeMaterielAdmin(admin.ModelAdmin):
    list_display = ('numero', 'beneficiaire', 'date', 'fournisseur')
    list_filter = ('date', 'fournisseur')
    search_fields = ('numero', 'beneficiaire__username', 'fournisseur__nom')
    inlines = [LigneDeCommandeInline]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('code_article', 'designation', 'prix_unitaire')
    search_fields = ('code_article', 'designation')

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact')
    search_fields = ('nom',)