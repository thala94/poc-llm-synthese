from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
import os
from datetime import datetime

def generate_pdf(text, output_dir="outputs" ):
    #Vérifier existance du dossier
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Génerer le nom du fichier selon date et heure 
    file_name = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    #chemin du fichier pdf
    file_path = os.path.join(output_dir, file_name)

    #Création du document PDF
    pdf = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    x = 50
    y = height - 50

    pdf.setFont("Helvetica", 11)
    # Parcours du texte ligne par ligne
    for line in text.split("\n"):

        wrapped_lines = wrap(line, width=90)

        if not wrapped_lines:
            wrapped_lines = [""]

        for wrapped_line in wrapped_lines:

            if y < 50:

                pdf.showPage()

                pdf.setFont("Helvetica", 11)

                y = height - 50

            pdf.drawString(x, y, wrapped_line)

            # Descend la position verticale pour la ligne suivante
            y -= 15

    # Sauvegarde finale du fichier PDF
    pdf.save()

    # Retourne le chemin du fichier généré
    return os.path.abspath(file_path)