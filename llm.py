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
        base_url="http://127.0.0.1:1234/v1",
        api_key="lm-studio" # nie trzeba prawdziwego api 
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
