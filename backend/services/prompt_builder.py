# Méthode pour construire le prompt selon le type de résumé demandé
def build_prompt(text, mode="resume_classique"):

    # Vérifie si le texte du document existe
    if not text:
        return None, {"error": "Texte manquant"}

    # =========================
    # Prompt système commun
    # =========================
    system_prompt = """
    Tu es un assistant spécialisé dans la synthèse documentaire ministérielle.

    Réponds uniquement en français.
    Respecte exactement la structure demandée.
    """

    # =========================
    # Résumé classique
    # =========================
    if mode == "resume_classique":

        user_prompt = f"""
        Fais un résumé clair, structuré et professionnel du document suivant.

        IMPORTANT :
        Utilise exactement le format ci-dessous.

        ## 1. Sujet principal
        ...

        ## 2. Idées importantes
        ...

        ## 3. Conclusion courte
        ...

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

        user_prompt = f"""
        Produis un résumé exécutif professionnel du document suivant.

        IMPORTANT :
        Utilise exactement le format ci-dessous.

        ## 1. Contexte
        ...

        ## 2. Objectif du document
        ...

        ## 3. Messages clés
        ...

        ## 4. Décisions ou éléments à retenir
        ...

        ## 5. Conclusion synthétique
        ...

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

        user_prompt = f"""
        Analyse le document suivant dans un contexte ministériel.

        IMPORTANT :
        Respecte exactement la structure ci-dessous.
        Ne fusionne pas les sections.
        Ne réponds pas sous forme d’un seul paragraphe.

        Utilise exactement ce format :

        ## 1. Contexte administratif
        ...

        ## 2. Objectif du document
        ...

        ## 3. Parties prenantes concernées
        ...

        ## 4. Enjeux principaux
        ...

        ## 5. Risques ou points de vigilance
        ...

        ## 6. Recommandations ou constats
        ...

        ## 7. Synthèse finale
        ...

        Le ton doit être :
        - professionnel
        - neutre
        - clair
        - structuré

        Document :
        {text[:4000]}
        """
        #{text}
    # =========================
    # Fiche synthèse
    # =========================
    elif mode == "fiche_synthese":

        user_prompt = f"""
        Transforme le document suivant en fiche synthèse claire et concise.

        IMPORTANT :
        Respecte exactement le format suivant.

        ## Titre du document
        ...

        ## Sujet
        ...

        ## Objectif
        ...

        ## Résumé
        ...

        ## Points importants
        ...

        ## Mots-clés
        ...

        ## Conclusion
        ...

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
            "error": "Mode invalide"
        }

    # Retourne prompts séparés
    return {
        "system": system_prompt,
        "user": user_prompt
    }, None