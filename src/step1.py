import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import cm

# Données de base du compte
NOM_BANQUE = "Banque Horizon"
NUM_COMPTE = "FR76 1234 5678 9012"
SOLDE_INITIAL = 500.0

# Descriptions réalistes de transactions
DESCRIPTIONS = [
    "Paiement carte - Supermarché",
    "Virement reçu - Salaire",
    "Retrait DAB",
    "Prélèvement EDF",
    "Paiement carte - Essence",
    "Abonnement Netflix",
    "Prélèvement Téléphone",
    "Virement envoyé - Colocataire",
    "Paiement carte - Restaurant",
    "Prélèvement Mutuelle",
    "Achat en ligne - Amazon",
    "Remboursement Sécurité Sociale",
    "Versement espèces",
    "Virement reçu - Ami",
    "Paiement carte - Boulangerie",
    "Achat en ligne - Cdiscount",
    "Virement reçu - Travaux",
    "Prélèvement Assurance Habitation",
    "Paiement carte - Magasin de vêtements",
    "Retrait ATM - Vacances",
    "Paiement carte - Libération de dépôt",
    "Virement - Remboursement prêt",
    "Retrait - Amis",
    "Achat - Meubles",
    "Prélèvement abonnements divers",
]

def generate_transactions(mois, annee, nb_transactions):
    """Génère une liste de transactions simulées pour un mois donné."""
    transactions = []
    solde = SOLDE_INITIAL

    for _ in range(nb_transactions):
        jour = random.randint(1, 28)
        date = datetime(annee, mois, jour)
        description = random.choice(DESCRIPTIONS)

        # Choisir un montant réaliste
        if "Salaire" in description or "reçu" in description or "Versement" in description:
            montant = round(random.uniform(500, 2000), 2)
        elif "Remboursement" in description:
            montant = round(random.uniform(10, 100), 2)
        else:
            montant = -round(random.uniform(5, 150), 2)

        solde += montant
        transactions.append({
            "date": date,
            "description": description,
            "montant": montant,
            "solde": round(solde, 2)
        })

    # Trier par date
    transactions.sort(key=lambda x: x["date"])
    return transactions

def generate_releve_pdf(mois, annee, nb_transactions):
    """Génère un relevé de compte PDF et retourne le chemin du fichier et le solde final."""
    transactions = generate_transactions(mois, annee, nb_transactions)
    solde_final = transactions[-1]["solde"] if transactions else SOLDE_INITIAL

    filename = f"releve_compte_{mois:02d}_{annee}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    elements = []

    # En-tête
    elements.append(Paragraph(f"<b>{NOM_BANQUE}</b>", styles["Title"]))
    elements.append(Paragraph(f"Relevé de compte - Mai {annee}", styles["Heading2"]))
    elements.append(Paragraph(f"Numéro de compte : {NUM_COMPTE}", styles["Normal"]))
    elements.append(Paragraph(f"Solde initial : {SOLDE_INITIAL:.2f} €", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Table des transactions
    data = [["Date", "Description", "Montant (€)", "Solde (€)"]]
    for tx in transactions:
        data.append([
            tx["date"].strftime("%d/%m/%Y"),
            tx["description"],
            f"{tx['montant']:.2f}",
            f"{tx['solde']:.2f}"
        ])

    table = Table(data, colWidths=[3*cm, 8*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Pied de page avec solde final
    elements.append(Paragraph(f"<b>Solde final : {solde_final:.2f} €</b>", styles["Normal"]))

    # Génération du PDF
    doc.build(elements)

    return filename, solde_final

# Exemple d’utilisation
if __name__ == "__main__":
    pdf_path, final_balance = generate_releve_pdf(mois=5, annee=2025, nb_transactions=40)
    print(f"Relevé généré : {pdf_path}")
    print(f"Solde final : {final_balance:.2f} €")