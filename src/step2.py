import random
import os
from datetime import datetime
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

# Constants
BANK_NAME = "Banque Horizon"
ACCOUNT_NUMBER = "FR76 1234 5678 9012"

# Transaction descriptions with their properties
TRANSACTION_DESCRIPTIONS = {
    "Paiement carte - Supermarché": (5, 150, "débit", 4),
    "Virement reçu - Salaire": (1500, 3000, "crédit", 1),
    "Retrait DAB": (20, 200, "débit", 2),
    "Prélèvement EDF": (30, 150, "débit", 1),
    "Paiement carte - Essence": (20, 100, "débit", 4),
    "Abonnement Netflix": (10, 20, "débit", 1),
    "Prélèvement Téléphone": (15, 50, "débit", 1),
    "Virement envoyé - Colocataire": (100, 800, "débit", 2),
    "Paiement carte - Restaurant": (15, 150, "débit", 3),
    "Prélèvement Mutuelle": (50, 200, "débit", 1),
    "Achat en ligne - Amazon": (5, 500, "débit", 3),
    "Remboursement Sécurité Sociale": (10, 100, "crédit", 2),
    "Versement espèces": (10, 200, "crédit", 2),
    "Virement reçu - Ami": (10, 100, "crédit", 2),
    "Paiement carte - Boulangerie": (5, 20, "débit", 4),
    "Paiement carte - Pharmacie": (5, 100, "débit", 2),
    "Prélèvement Internet": (30, 100, "débit", 1),
    "Virement reçu - Assurance": (50, 200, "crédit", 1),
    "Paiement carte - Cinéma": (10, 50, "débit", 2),
    "Récompense cashback": (1, 20, "crédit", 2),
    "Prélèvement Gym": (20, 100, "débit", 2),
    "Remboursement impôts": (50, 200, "crédit", 1),
    "Paiement carte - Librairie": (5, 50, "débit", 1),
    "Dépôt chèque": (50, 1000, "crédit", 1),
    "Virement interne - Épargne": (10, 500, "débit", 1),
}

def generate_transactions(month, year, num_transactions, initial_balance):
    """
    Generate a list of transactions for a given month and year.

    Args:
        month (int): The month for which to generate transactions.
        year (int): The year for which to generate transactions.
        num_transactions (int): The number of transactions to generate.
        initial_balance (float): The initial balance of the account.

    Returns:
        list: A list of dictionaries, each representing a transaction.
    """
    transactions = []
    balance = initial_balance
    credits = 0
    debits = 0
    transaction_counts = {desc: 0 for desc in TRANSACTION_DESCRIPTIONS.keys()}

    while len(transactions) < num_transactions:
        day = random.randint(1, 28)
        date = datetime(year, month, day)
        description, (min_amount, max_amount, transaction_type, freq) = random.choice(list(TRANSACTION_DESCRIPTIONS.items()))

        if transaction_counts[description] < freq:
            amount = round(random.uniform(min_amount, max_amount), 2)
            if transaction_type == "débit":
                amount = -amount

            if amount > 0:
                credits += amount
            else:
                debits += abs(amount)

            transactions.append({
                "date": date,
                "description": description,
                "amount": amount,
            })

            transaction_counts[description] += 1

    transactions.sort(key=lambda x: x["date"])

    for transaction in transactions:
        balance += transaction["amount"]
        transaction["balance"] = round(balance, 2)

    return transactions

def generate_pdf_statement(month, year, num_transactions, output_dir="output", initial_balance=0):
    """
    Generate a PDF statement for a given month and year.

    Args:
        month (int): The month for which to generate the statement.
        year (int): The year for which to generate the statement.
        num_transactions (int): The number of transactions to generate.
        output_dir (str): The directory in which to save the PDF.
        initial_balance (float): The initial balance of the account.

    Returns:
        tuple: A tuple containing the path to the generated PDF and the final balance.
    """
    initial_balance = initial_balance
    transactions = generate_transactions(month, year, num_transactions, initial_balance)
    final_balance = transactions[-1]["balance"] if transactions else initial_balance

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"releve_compte_{month:02d}_{year}_{ACCOUNT_NUMBER[-3:]}.pdf"
    filepath = f"{output_dir}/{filename}"
    doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"<b>{BANK_NAME}</b>", styles["Title"]))
    elements.append(Paragraph(f"Relevé de compte - {month:02d}/{year}", styles["Heading2"]))
    elements.append(Paragraph(f"Numéro de compte : {ACCOUNT_NUMBER}", styles["Normal"]))
    elements.append(Paragraph(f"Solde initial : {initial_balance:.2f} €", styles["Normal"]))
    elements.append(Spacer(1, 12))

    data = [["Date", "Description", "Montant (€)", "Solde (€)"]]
    for tx in transactions:
        data.append([
            tx["date"].strftime("%d/%m/%Y"),
            tx["description"],
            f"{tx['amount']:.2f}",
            f"{tx['balance']:.2f}"
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

    elements.append(Paragraph(f"<b>Solde final : {final_balance:.2f} €</b>", styles["Normal"]))

    doc.build(elements)

    return filepath, final_balance

def main():
    """
    Main function to generate PDF statements for a range of months and years.
    """
    start_month = 1
    start_year = 2024
    end_month = 12
    end_year = 2024
    num_transactions_per_month = 40

    current_year = start_year
    current_month = start_month
    initial_balance = 0

    while current_year < end_year or (current_year == end_year and current_month <= end_month):
        pdf_path, final_balance = generate_pdf_statement(
            month=current_month,
            year=current_year,
            num_transactions=num_transactions_per_month,
            initial_balance=initial_balance
        )
        print(f"Relevé généré : {pdf_path} pour {current_month:02d}/{current_year}")
        print(f"Solde final : {final_balance:.2f} €")

        initial_balance = final_balance
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

if __name__ == "__main__":
    main()
