from openai import OpenAI

# jak chujowe wyniki to zjebalem spojnosc41-50
def llm_query(prompt: str, model_id: str, temperature: float = 0.8) -> str:
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
        alt_text += f"Alternative {i+1}: Price in euros ={alt[0]}, RAM size in GB ={alt[1]}, CPU frequency ={alt[2]}, Storage in GB ={alt[3]}, weight in KG={alt[4]}, screen size in inches ={alt[5]}\n"

# Nowy prompt bez sugestii eksperta
# do wersji z sugestia dodac : BUSINESS GOAL: Maximize the number of people who will use this charging station.

        # Wybierz sugestie
        #goal = "None, just pick the best laptop overall."
        #goal = "Find the best laptop for gaming."
        #goal = "Find the most budget-friendly laptop for everyday tasks."
        #goal = "Find the best laptop for work."
        #goal = "Find the best laptop for programming and software development."
        #goal = "Find the lightest, most compact laptop suitable for frequent travel."
        #goal = "Find the best laptop for graphic design and video editing."
        #goal = "Find the best laptop for a mix of gaming and work."
        #goal = "Find the best laptop for students on a budget."
        #goal = "Find the best laptop for business professionals."
        #goal = "Find the best laptop for casual use and media consumption."
        #goal = "Find the absolute cheapest laptop possible, regardless of performance."
        #goal = "Find the most powerful laptop for intensive computational tasks like AI training."
        goal = "None, just pick the best laptop overall."

        prompt = f"""
        You are choosing the optimal laptop. And create a ranking of alternatives from best to worst based on the BUSINESS GOAL and criteria below.

BUSINESS GOAL: {goal}

Each alternative is a laptop with the following attributes:
- price in euros (lower is better if budget is important)
- RAM size in GB (higher is better if performance is important)
- CPU freq in GHz (higher is better for performance)
- storage type and size (larger capacity is better)
- weight in kg (lighter is better for portability)
- screen size in inches (smaller is better for mobility, larger is better for gaming and work)

Alternatives:
{alt_text}

Think: Decide which laptop fits the goal better.  
Do not always pick based on price - interpret the goal and decide what matters most.  

Before choosing, answer:
- Which laptop better serves the goal?
- What specific advantages does each offer for goal?
Then choose based on goal requirements.

Answer only with a list of alternative numbers in order from best to worst, separated by commas. 
Do not include any additional text. Do not explain or justify your ranking.
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
    
    print(f"Prompt do LLM:\n{prompt}")
    odpowiedz = llm_query(prompt, model_id)

    return odpowiedz
