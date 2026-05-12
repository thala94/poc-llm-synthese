# Méthode pour construire le prompt selon le type de résumé demandé
def build_prompt(text, mode="resume_classique"):

    # Vérifie si le texte du document existe
    if not text:
        return None, {"error": "Texte manquant"}

    # =========================
    # Résumé classique
    # =========================
    if mode == "resume_classique":

        prompt = f"""
        Tu es un assistant spécialisé dans la synthèse documentaire.

        Réponds uniquement en français.
        Tous les titres et toutes les sections doivent être en français.

        Fais un résumé clair, structuré et professionnel du document suivant.

        Structure attendue :

        1. Sujet principal
        2. Idées importantes
        3. Conclusion courte

        Le résumé doit être :
        - synthétique
        - facile à comprendre
        - rédigé dans un style professionnel

        Document :
        {text}
        """

    # =========================
    # Résumé exécutif
    # =========================
    elif mode == "resume_executif":

        prompt = f"""
        Tu es un assistant spécialisé dans les résumés exécutifs.

        Réponds uniquement en français.

        Produis un résumé exécutif professionnel du document suivant.

        Structure attendue :

        1. Contexte
        2. Objectif du document
        3. Messages clés
        4. Décisions ou éléments à retenir
        5. Conclusion synthétique

        Le résumé doit :
        - aller à l’essentiel
        - être rédigé dans un style administratif
        - mettre en évidence les informations importantes

        Document :
        {text}
        """

    # =========================
    # Analyse ministérielle
    # =========================
    elif mode == "analyse_ministerielle":

        prompt = f"""
        Tu es un analyste spécialisé dans les documents ministériels.

        Réponds uniquement en français.
        Même si le document contient des mots anglais,
        la réponse finale doit être entièrement en français.

        Analyse le document suivant dans un contexte ministériel.

        Structure attendue :

        1. Contexte administratif
        2. Objectif du document
        3. Parties prenantes concernées
        4. Enjeux principaux
        5. Risques ou points de vigilance
        6. Recommandations ou constats
        7. Synthèse finale

        Le ton doit être :
        - professionnel
        - neutre
        - clair
        - structuré

        Document :
        {text}
        """

    # =========================
    # Fiche synthèse
    # =========================
    elif mode == "fiche_synthese":

        prompt = f"""
        Tu es un assistant spécialisé dans les fiches synthèse.

        Réponds uniquement en français.

        Transforme le document suivant en fiche synthèse claire et concise.

        Format attendu :

        - Titre du document
        - Sujet
        - Objectif
        - Résumé en quelques lignes
        - Points importants
        - Mots-clés
        - Conclusion

        Le résultat doit être :
        - facile à lire
        - structuré
        - synthétique

        Document :
        {text}
        """

    # =========================
    # Mode invalide
    # =========================
    else:

        return None, {
            "error": "Mode invalide. Utilise : resume_classique, resume_executif, analyse_ministerielle ou fiche_synthese."
        }

    # Retourne le prompt final
    return prompt, None