from django import forms
from django.forms import inlineformset_factory
from .models import DemandeDeMateriel, Fournisseur, LigneDeCommande, Article

class DemandeDeMaterielForm(forms.ModelForm):
    class Meta:
        model = DemandeDeMateriel
        # 'beneficiaire' est retiré des champs
        fields = ['justification', 'nature_des_prestations', 'fournisseur', 'imputation', 'credit']
        widgets = {
            'justification': forms.Textarea(attrs={'class': 'modern-textarea', 'rows': 4}),
            'nature_des_prestations': forms.Select(attrs={'class': 'modern-select'}),
            'fournisseur': forms.Select(attrs={'class': 'modern-select'}),
        }

LigneDeCommandeFormSet = inlineformset_factory(
    DemandeDeMateriel,
    LigneDeCommande,
    fields=('article', 'quantite'),
    extra=1,
    can_delete=True
)