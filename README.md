1. Połączyć się z maszyną `192.168.205.44`
2. Uruchomić serwer ollama `ollama serve`
3. Wpisać IP serwera ollama w pliku `llm.py` w sekcji:
```python
client = OpenAI(
        base_url="http://127.0.0.1:11434/v1",
        api_key="ollama" # nie trzeba prawdziwego api 
    )
```
4. Sprawdzić czy nasz model jest pobrany
```bash
ollama list
```



#### `llm.py`

Plik zawiera prostą funkcję `llm_query`, która odpowiada za komunikację z lokalnie hostowanym LLM przez API OpenAI.

- Łączy się z serwerem LM Studio (`http://127.0.0.1:1234/v1`).
- Nie wymaga prawdziwego klucza API (wstawiony `"lm-studio"`).
- Przyjmuje:
    - `prompt` – treść zapytania,
    - `model_id` – nazwa modelu uruchomionego lokalnie,
    - `temperature` – kontrola losowości generacji.
- Zwraca odpowiedź LLM jako string.
    
- W `__main__` dodany test, który wysyła pytanie o stolicę Japonii i wypisuje odpowiedź.
---

#### `llm_expert.py`

Plik definiuje klasę `LLMExpert`, która zastępuje `ManualExpert` z `pymcdm` i zmienia sposób zadawania pytań ekspertowi.

- Dziedziczy po `ManualExpert`.
- Konstruktor:
    - wymaga `model_id` (nazwa modelu do zapytań),
    - wymaga `criteria_names` (lista kryteriów, przekazywana dalej do `ManualExpert`).
- Dodaje licznik pytań (`self.pytanie_nr`).

**Nadpisana metoda `_query_user`:**

- Wywoływana automatycznie przez COMET do porównań obiektów charakterystycznych.
- Zamiast pytać człowieka, buduje prompt i wysyła porównanie do LLM:
    - Obiekt A (`co1`) vs Obiekt B (`co2`),
    - pytanie zawsze w formie „Który obiekt jest lepszy? Odpowiedz dokładnie A lub B”.
- Wynik LLM (`"A"` lub `"B"`) mapowany na:
    - `1` → `co1` wygrywa,
    - `0` → `co2` wygrywa.
- Każde zapytanie i odpowiedź wypisywane są w konsoli.
---
#### `main.py`
 Główny skrypt uruchamiający ocenę alternatyw za pomocą metody COMET i eksperta LLM.
- Importuje niezbędne biblioteki: `numpy` do obliczeń numerycznych, `COMET` z `pymcdm.methods` oraz własną klasę `LLMExpert`.

- Funkcja `main()` uruchamia cały proces:
    1. Wyświetla nagłówek informacyjny i definiuje wartości charakterystyczne (`cvalues`) dla każdego kryterium określa trzy poziomy oceny (min, średni, max).
    2. Oblicza liczbę wszystkich obiektów charakterystycznych oraz liczbę par porównań wymaganych w COMET.
    3. Wskazuje model LLM (`model_id`) używany do oceny preferencji.
    4. Tworzy eksperta LLM (`LLMExpert`), który zastępuje klasycznego eksperta manualnego.
    5. Tworzy instancję modelu COMET z wartościami charakterystycznymi i ekspertem LLM.
    6. Definiuje zestaw alternatyw do oceny i wywołuje model COMET, aby uzyskać preferencje.
    7. Wyświetla wyniki oceny alternatyw oraz ranking od najlepszej do najgorszej alternatywy wraz z ich wartościami punktowymi.
- Skrypt jest w pełni interaktywny w terminalu - pokazuje wszystkie kroki, wartości pośrednie oraz końcowe wyniki w czytelnej formie.
- Uruchamiany bezpośrednio (`if __name__ == "__main__": main()`).

---


#### Flow działania

1. COMET w trakcie budowania modelu wywołuje `_query_user`.
2. `LLMExpert` zamiast człowieka wysyła pytanie do modelu LLM.
3. Odpowiedź LLM jest parsowana i zwracana w formacie zgodnym z `ManualExpert`.
4. Dzięki temu COMET korzysta z LLM jako automatycznego eksperta w procesie porównań.
