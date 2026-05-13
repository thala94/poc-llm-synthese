import os
from flask import Flask, request, jsonify, send_file
import requests
from services.pdf_reader import read_pdf
from services.prompt_builder import build_prompt
from services.pdf_exporter import generate_pdf

app = Flask(__name__)


# Méthode commune pour appeler le modèle LLM local avec Ollama
def ask_llm(system_prompt, user_prompt ,model="mistral"):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "stream": False
        }
    )
    return response.json()

# Méthode pour récupérer la liste des modèles installés dans Ollama
def get_models():

    response = requests.get(
        "http://localhost:11434/api/tags"
    )

    data = response.json()

    models = []

    for model in data["models"]:
        models.append(model["name"])

    return models

# Définition des routes 
@app.route("/")
def home():
    return {"message": "API Flask OK"}

@app.route("/models", methods=["GET"])
def models():
    result = get_models()
    return jsonify({
        "models": result
    })

#Route pour poser une question  
# Note revérifier le mode 
@app.route("/ask", methods=["POST"])
def ask():

    #Récupérer les données envoyer par le client, et la question
    data = request.get_json()
    question = data.get("question", "")
    mode = data.get("mode", "resume_classique")

    #Appler la methode pour construire le prompt 
    prompt, error = build_prompt(
        text = question, 
        mode= mode
    )

    if error:
        return jsonify(error), 400

    result = ask_llm(
    system_prompt=prompt["system"],
    user_prompt=prompt["user"]
)
    return result


#Route pour résumé un pdf 
@app.route("/resume", methods=['POST'])
def resume() :
    #Récupérer les données envoyer par le client, chemin du pdf,  model
    data = request.get_json()
    #Cemn du fichier pdf
    file_path = data.get("file_path", "")
    mode = data.get("mode", "resume_classique")
    model = data.get("model", "mistral")

    if not file_path : 
        return jsonify(file_path)
     #Appler la methode pour construire le prompt 
    text = read_pdf(file_path)

    if not text:
        return jsonify({"error": "Aucun texte trouvé dans le PDF"}), 400
    
    prompt, error = build_prompt(
        text = text, 
        mode= mode
    )

    if error:
        return jsonify(error), 400

    result = ask_llm(
                    system_prompt=prompt["system"],
                    user_prompt=prompt["user"],
                    model=model
    )

    download = data.get("download", False)

    generate_text = result["message"]["content"]

    if download:
        pdf_path = generate_pdf(generate_text)
        print(pdf_path)
        print(os.path.exists(pdf_path))
        print("PDF PATH =", pdf_path)
        print("EXISTS =", os.path.exists(pdf_path))
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="resume.pdf",
            mimetype="application/pdf"
        )

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)