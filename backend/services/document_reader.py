from services.pptx_reader import read_pptx
from services.word_reader import read_word
from services.pdf_reader import read_pdf
import os

def read_document(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    elif extension == ".pptx":
        return read_pptx(file_path)
    
    elif extension ==".docx":
        return read_word(file_path)

    else:
        raise ValueError("Format non supporté. Utilise PDF ou PPTX ou DOC.")
    
    