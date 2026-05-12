from pypdf import PdfReader
# Lire un fichier pdf 
def read_pdf(file_path):
    reader = PdfReader(file_path)
    # Stockage du texte extrait du pdf
    text = ""
    #  Extraire toutes les pages du document
    for page in reader.pages : 
        # extraire le texte de la page courante
        page_text = page.extract_text()

        # Vérifier disponibilité de l'extraction
        if page_text:
            text += page_text + "/n"
    print ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",text)
    return text




