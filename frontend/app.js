//Zone d'affichage des logs lors du traitement des documents
const logsBox = document.getElementById("logs");
// Ajout de ligne dans le log
function addLog(message) {
    logsBox.textContent += message + "\n";
}

// Récupère le bouton et la zone d'affichage
const generateBtn = document.getElementById("generateBtn");
const resultBox = document.getElementById("result");

//Événement lors du clique du bouton
generateBtn.addEventListener("click", async () => {
     // Réinitialise le log
    logsBox.textContent = "";

    // Début du chronomètre
    const startTime = Date.now();
    //désactiver le bouton pendant le traitement et modifier son texte
    generateBtn.disabled = true; 
    resultBox.textContent = "Génération du résumé en cours...";
    generateBtn.textContent = "En Traitement...";

    //Mise en place des logs à afficher à l'écran
    addLog("Lecture des documents...");
    //Récupérer les valeurs du formulaire
    const filePathsText = document.getElementById("filePaths").value;
    const mode = document.getElementById("mode").value;
    const model = document.getElementById("model").value;
    const download = document.getElementById("download").checked;
    //transformation des chemins en tableau
    const filePaths = filePathsText
        .split("\n")
        .map(path => path.trim())
        .filter(path => path !== "");

    // Nombre de documents détectés
    addLog(filePaths.length + " document(s) détecté(s)");    
    // Création des données JSON
    const payload = {
        file_paths: filePaths,
        mode: mode,
        model: model,
        download: download
    };

    // Appel API Flask
    try {
        addLog("Construction du prompt...");
        addLog("Envoi au modèle : " + model);

        const response = await fetch("http://127.0.0.1:5000/resume", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (download) { //Cas téléchargement de documents
            addLog("Génération du PDF...");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const link = document.createElement("a");
            link.href = url;
            link.download = "resume_documents.pdf";
            link.click();

            window.URL.revokeObjectURL(url);

            resultBox.textContent = "PDF téléchargé avec succès.";
            addLog("PDF téléchargé avec succès.");

        } else { //Affichage du texte dans l'écran
            const data = await response.json();

            if (data.error) {
                resultBox.textContent = "Erreur : " + data.error;
            } else {
                resultBox.textContent = data.result;
                addLog("Résumé généré avec succès.");
            }
        }
         // Temps total
        const endTime = Date.now();

        const duration =
            ((endTime - startTime) / 1000).toFixed(2);

        addLog(
            "Temps total : " +
            duration +
            " secondes"
        );
    } catch (error) {
        resultBox.textContent = "Erreur de connexion avec Flask : " + error.message;
        addLog(
            "Erreur de connexion avec Flask");
    }
    finally {

        generateBtn.disabled = false;

        generateBtn.textContent =
            "Générer le résumé";
    }
});