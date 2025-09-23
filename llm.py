from openai import OpenAI

def llm_query(prompt: str, model_id: str, temperature: float = 0.3) -> str:
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
        {"role": "system", "content": "Jesteś ekspertem do spraw wspomagania decyzji wielokryterialnych."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        completion = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=temperature
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
    
    # Przygotuj opis alternatyw
    alt_text = ""
    for i, alt in enumerate(alternatives):
        alt_text += f"{i+1}. koszt={alt[0]}, jakość={alt[1]}, dostępność={alt[2]}\n"
    # Prompt z Sugestia eksperta
#     prompt = f"""
# You are an expert in multi-criteria decision making.  
# Here are several alternatives, each described by the same set of criteria:
# y
# Criteria: distance_to_parking_meters_lower_better, distance_to_roads_meters_lower_better, distance_to_charging_stations_meters_lower_better, number_of_nearby_shops_higher_better, number_of_nearby_restaurants_higher_better, population_density_higher_better

# Alternatives:  
# {alt_text}

# Consider that our goal is to place NEW electric car chargers station in place available to as many people as possible and to allow them to spend their free time while charging. Based on this goal, decide which criteria are more important and use this to determine the ranking    .  

# Task: Rank all the alternatives from best to worst according to your expert judgment.  
# Answer with the indices in order, separated by commas
# Do not provide any explanation or additional text. 
# """
    
    # Prompt bez sugestii eksperta
    prompt = f"""
    You are an expert in multi-criteria decision making.

Here are several alternatives, each described by the same set of criteria:

Criteria types: cost (to minimize) and benefit(to maximize)

Criteria: distance_parking (cost), distance_roads (cost), distance_stations (cost), shops (benefit), restaurants (benefit), population_density (benefit)

Alternatives:
{alt_text}

Task: Rank all the alternatives from best to worst according to your expert judgment.

Answer with the indices in order, separated by commas

Do not provide any explanation or additional text.
    """
    odpowiedz = llm_query(prompt, model_id)

    return odpowiedz
