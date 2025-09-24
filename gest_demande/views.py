from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import DemandeDeMateriel, Fournisseur
from .forms import DemandeDeMaterielForm, LigneDeCommandeFormSet

def index(request):
    return render(request, 'gest_demande/index.html')

@login_required
def nouvelle_demande(request):
    if request.method == 'POST':
        form = DemandeDeMaterielForm(request.POST)
        formset = LigneDeCommandeFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            demande = form.save(commit=False)
            
            # Attribue l'utilisateur actuel comme bénéficiaire de la demande
            demande.beneficiaire = request.user
            
            demande.numero = f"DEM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            demande.save()
            
            formset.instance = demande
            formset.save()
            
            return redirect('generer_quittance', demande_id=demande.id)
    else:
        form = DemandeDeMaterielForm()
        formset = LigneDeCommandeFormSet()

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'gest_demande/nouvelle_demande.html', context)

def generer_quittance(request, demande_id):
    demande = get_object_or_404(DemandeDeMateriel, pk=demande_id)
    lignes = demande.lignes.all()
    
    context = {
        'demande': demande,
        'lignes': lignes,
    }

    html_string = render_to_string('gest_demande/quittance_pdf.html', context)
    
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[CSS(string='''
        @page { size: A4; margin: 2cm; }
        body { font-family: sans-serif; }
        .header { text-align: center; margin-bottom: 2cm; }
        .details { margin-bottom: 1cm; }
        .table-articles { width: 100%; border-collapse: collapse; }
        .table-articles th, .table-articles td { border: 1px solid #000; padding: 8px; text-align: left; }
        .total { text-align: right; margin-top: 2cm; }
    ''')])

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="quittance_demande_{demande.numero}.pdf"'

    return response