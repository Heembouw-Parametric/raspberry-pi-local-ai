import requests


def request_llm(vraag: str) -> str:
    # OpenAI API request
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }

    data = {
        "model": "gpt-4o-mini",  # of gpt-4o / gpt-3.5-turbo
        "messages": [
            {"role": "system", "content": """
            Je bent een assistent die alleen vragen over Heembouw, Ruud van Berkel (oprichter Heembouw) en de Ruud van Berkel Award (innovatieprijs) beantwoordt.
            Antwoord altijd in het Nederlands, duidelijk en maximaal 100 woorden, voorkeur lengte van een tweet.
            Als de vraag niet over Heembouw gaat, zeg dan dat je daar geen antwoord op kunt geven en geef je tips waar de gebruiker wel vragen over kan stellen.
            """},

            {"role": "user", "content": f"{vraag}"},
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    print(result["choices"][0]["message"]["content"])
    return result["choices"][0]["message"]["content"]

