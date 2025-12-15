from django.http import JsonResponse
import random
import openai
import os

POE_API_KEY = os.getenv("POE_API_KEY", "v5HTr2OJhTHhliM2BgNW348IByS2WB04i4c7-dOaLVs")

PROMPT_PATHOCE = """
Tu es Patrick « Patoche » Dupont, 57 ans, mécano retraité de Seine-Saint-Denis, père de 4 morveux, marié à une 405 break diesel de 1991 que tu appelles « la bête ». Tu portes un marcel taché, tu bois du pastis 51 sans glaçons, tu fumes des Gauloises sans filtre. Tu es convaincu que tout était mieux avant 95 et que tous les problèmes se règlent avec du WD-40, du chatterton et un bon coup de pied dans le starter.

RÈGLES DE FER (jamais les briser) :
1. Tu NE RÉPONDS JAMAIS à la question posée. Jamais. Même si on te menace.
2. Tu pars direct dans une anecdote des années 80-90 complètement hors sujet.
3. Tu donnes toujours un conseil de daron dangereux et inutile qui finit par « et voilà le travail ».
4. Tu finis souvent par « mon grand », « espèce de zozo », « p’tit malin », « j’te jure ma p’tite dame ».
5. Tu répètes sans cesse : « À mon époque… », « Moi en 92… », « Ta génération vous êtes des assistés », « la bête elle démarre encore au quart de tour ».
6. Langage 100 % daron : « bah ouais », « force forcément », « attends j’te dis pas la suite », « j’vais chercher une Kro ».
"""

client = openai.OpenAI(
    api_key=POE_API_KEY,
    base_url="https://api.poe.com/v1"
)


def ask_patoche(request):
    question = request.GET.get("msg", "").strip()
    if not question:
        return JsonResponse({"reponse": "Bah alors, t’as perdu ta langue, mon grand ?"})

    # Réponses locales au cas où Poe tombe en rade
    fallback_reponses = [
        "Ton CV ? À mon époque, on écrivait ça au stylo Bic sur la nappe du PMU, et voilà le travail, mon grand.",
        "Si ton CV mentionne que tu sais redémarrer une 405 en pente, c'est embauche directe, espèce de zozo.",
        "Moi en 92, mon CV c’était : ‘sait manier le marteau, le Ricard et le démarreur’… Et ça suffisait largement.",
        "Tu mets juste ‘sait réparer avec du scotch et du WD-40’, et crois-moi, ça impressionne plus que ton PowerPoint.",
    ]

    try:
        response = client.chat.completions.create(
            model="claude-sonnet-4.5",
            messages=[
                {"role": "system", "content": PROMPT_PATHOCE},
                {"role": "user", "content": question},
            ],
            temperature=0.9,
            max_tokens=300,
        )
        reponse = response.choices[0].message.content.strip()

    except Exception as e:
        # 🔥 Ici tu vois la vraie erreur dans la console Django
        print(f"[ERREUR] Panne totale : {type(e).__name__} - {e}")
        # 👉 mais pour le front, on envoie quand même une réponse rigolote
        reponse = random.choice(fallback_reponses)

    return JsonResponse({"reponse": reponse})
