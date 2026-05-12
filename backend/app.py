from flask import Flask, request, jsonify
import requests
from services.pdf_reader import read_pdf
from services.prompt_builder import build_prompt


app = Flask(__name__)


# Méthode commune pour appeler le modèle LLM local avec Ollama
def ask_llm(prompt, model="mistral"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
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

    result = ask_llm(prompt)
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
    
    #test pour voir le texte extrait
    
    prompt, error = build_prompt(
        text = text, 
        mode= mode
    )

    if error:
        return jsonify(error), 400

    print("MODE =", mode)
    print("MODEL =", model)
    print("PROMPT =", prompt[:1000])

    result = ask_llm(prompt, model=model)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)