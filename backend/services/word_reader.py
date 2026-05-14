from docx import Document


# Méthode pour lire un fichier Word (.docx)
def read_word(file_path):

    # Ouvre le document Word
    doc = Document(file_path)

    text = ""

    # Parcours tous les paragraphes
    for paragraph in doc.paragraphs:

        # Ajoute le texte du paragraphe
        text += paragraph.text + "\n"

    return text