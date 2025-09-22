# COMET+LLM

System porównywania decyzji wielokryterialnych używający COMET z ekspertem LLM zamiast człowieka.

## Pliki

**llm.py** - komunikacja z LLM przez API OpenAI. Funkcja `llm_query()` wysyła prompt do lokalnego serwera ollama i zwraca odpowiedź.

**llm_expert.py** - klasa `LLMExpert` dziedzicząca po `ManualExpert` lub `TriadSupportExpert` z biblioteki pymcdm. Zamiast pytać człowieka o porównania, wysyła zapytania do LLM. Każde porównanie to "Który obiekt lepszy? A czy B?".

**main.py** - główny skrypt. Tworzy model COMET z LLMExpert, definiuje alternatywy i wartości charakterystyczne, uruchamia ocenę i pokazuje ranking.

**direct_ranking.py** - porównuje wyniki COMET+LLM z bezpośrednim zapytaniem do LLM o ranking. Trzeba ręcznie wpisać ranking z main.py.

## Uruchamianie

1. Uruchom serwer ollama: `ollama serve`
2. Sprawdź dostępne modele: `ollama list` 
3. Zmień IP serwera w `llm.py` jeśli potrzeba:
```python
base_url="http://127.0.0.1:11434/v1"
```
4. Ustaw model_id w `main.py`:
```python
model_id = "llama3.2:3b"
```
5. Uruchom: `python main.py`

## Zmienianie parametrów

**Alternatywy** - zmień w `main.py` i `direct_ranking.py` tablicę `alternatives`. Po zmianie trzeba uruchomić main.py i przepisać ranking do direct_ranking.py.

**Wartości charakterystyczne** - zmień `cvalues` w `main.py`. Więcej poziomów = więcej porównań dla LLM.

**Kryteria** - zmień nazwy w `LLMExpert(criteria_names=["cost","quality","availability"])`.

## Flow działania

1. COMET generuje wszystkie obiekty charakterystyczne z `cvalues`
2. Dla każdej pary obiektów wywołuje `LLMExpert._query_user()`  
3. LLMExpert wysyła porównanie do LLM: "Obiekt A vs B, który lepszy?"
4. Odpowiedź LLM mapowana na 1 (A wygrywa) lub 0 (B wygrywa)
5. COMET buduje model preferencji z odpowiedzi LLM
6. Model ocenia prawdziwe alternatywy i zwraca ranking
