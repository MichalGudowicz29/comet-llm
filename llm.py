from openai import OpenAI

def llm_query(prompt: str, model_id: str, temperature: float = 0.0) -> str:
    """
    Funkcja do wysyłania zapytań do LLM przez LM Studio.
    
    Args:
        prompt: Tekst zapytania do LLM
        model_id: ID modelu (np. z http://127.0.0.1:1234/v1/models)
        temperature: Parametr temperatury (0.1-0.3 przewidywalne, 0.7-1.0 kreatywne)
    
    Returns:
        Odpowiedź LLM jako string
    """
    # Klient OpenAI skonfigurowany dla LM Studio
    client = OpenAI(
        base_url="http://127.0.0.1:11434/v1",
        api_key="ollama" # nie trzeba prawdziwego api 
    )
    
    messages = [
        {"role": "system", "content": "You are an expert in multi-criteria decision making."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        # completion = client.chat.completions.create(
        #     model=model_id,
        #     messages=messages,
        #     temperature=temperature
        # )
        # Proba innego completion (proba optymalizacji)
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are an expert in multi-criteria decision making."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            #max_tokens=5,  # Tylko A lub B
            #stop=["\n", ".", " "]  # Zatrzymaj natychmiast
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Błąd komunikacji z LLM: {e}")
        return "Błąd komunikacji"


# Przykład testowy
if __name__ == "__main__":
    # Test funkcji
    test_prompt = "Jaka jest stolica Japonii?"
    model_name = "bielik-1.5b-v3.0-instruct"
    
    odpowiedz = llm_query(test_prompt, model_name)
    print(f"Pytanie: {test_prompt}")
    print(f"Odpowiedź: {odpowiedz}")



def direct_llm_ranking(alternatives, model_id):
    """Bezpośrednio pyta LLM o ranking"""
    
    alt_text = ""
    for i, alt in enumerate(alternatives):
        alt_text += f"Alternative {i+1}: distance_to_parking={alt[0]}, distance_to_roads={alt[1]}, distance_to_charging_stations={alt[2]}, nearby_shops={alt[3]}, nearby_restaurants={alt[4]}, population_density={alt[5]}\n"

# Nowy prompt bez sugestii eksperta
# do wersji z sugestia dodac : BUSINESS GOAL: Maximize the number of people who will use this charging station.

    prompt = f"""
You are choosing the optimal location for an EV charging station.  
Rank ALL given alternatives from BEST to WORST.  
You MUST output ALL indices exactly once. 

criteria:
- distance_parking in meters (lower is better)
- distance_roads in meters (lower is better)
- distance_stations in meters (lower is better)
- shops (number of nearby shops within 500m, higher is better)
- restaurants (number of nearby restaurants within 500m, higher is better)
- population_density (number of residental houses within 500m, higher is better) 


Alternatives:
{alt_text}

Return ONLY the indices of ALL alternatives in ranking order, separated by commas. Do not explain or justify.

"""

# Nowy prompt z sugestia eksperta
#     prompt = f"""
# You are an expert in multi-criteria decision making.

# Criteria: 
# - distance_parking: distance to nearest parking (meters)
# - distance_roads: distance to main roads (meters) 
# - distance_stations: distance to existing charging stations (meters)
# - shops: number of nearby shops within 500m
# - restaurants: number of nearby restaurants within 500m
# - population_density: number of residental houses within 500m
# Alternatives:
# {alt_text}

# Consider that our goal is to make car chargers available to as many people as possible and to allow them to spend their free time while charging. Based on this goal, decide which criteria are more important and use this to determine the ranking.

# Rank all alternatives from best to worst. Answer with indices in order, separated by commas.
# """
    
    odpowiedz = llm_query(prompt, model_id)

    return odpowiedz
