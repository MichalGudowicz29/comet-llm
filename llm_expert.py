import numpy as np
from pymcdm.methods.comet_tools import ManualExpert
from llm import llm_query
import re


class LLMExpert(ManualExpert):
    """
    klasa, która zastępuje ręczne odpowiedzi eksperta odpowiedziami LLM
    """
    def __init__(self, model_id: str, criteria_names):
        super().__init__(criteria_names)
        self.model_id = model_id
        self.pytanie_nr = 0
    
    def _query_user(self, co1_name: str, co2_name: str) -> int:
        """
        Metoda wywoływana przez COMET do porównania dwóch obiektów charakterystycznych.
        Zwraca 1 jeśli co1 > co2, 0 jeśli co1 < co2
        """
        self.pytanie_nr += 1
        print(f"\n--- Pytanie {self.pytanie_nr} ---")
        
        # Znajdź indeksy obiektów
        co1_idx = list(self.co_names).index(co1_name)
        co2_idx = list(self.co_names).index(co2_name)
        
        # Pobierz rzeczywiste wartości
        co1_values = self.characteristic_objects[co1_idx]
        co2_values = self.characteristic_objects[co2_idx]

        prompt = f"""
Jesteś ekspertem wybierającym lepszy obiekt.

Obiekt A: koszt={co1_values[0]}, jakość={co1_values[1]}, dostępność={co1_values[2]}
Obiekt B: koszt={co2_values[0]}, jakość={co2_values[1]}, dostępność={co2_values[2]}

Zasady oceny:
- niższy koszt = lepiej
- wyższa jakość = lepiej
- wyższa dostępność (0–10) = lepiej
- dostępność=0 oznacza całkowity brak dostępności = bardzo źle

**Instrukcja:** Po przeanalizowaniu wszystkich kryteriów, odpowiedź **wyłącznie jedną literą**: A lub B.  
Nie pisz nic więcej, żadnego uzasadnienia, żadnego komentarza.  
Twoja odpowiedź musi być jednoznaczna.
"""
        print(f"Porównuję: {co1_name} {co1_values} vs {co2_name} {co2_values}")

        odpowiedz = llm_query(prompt, self.model_id)
        odpowiedz_clean = odpowiedz.strip().upper()
        if "A" in odpowiedz_clean:
            print("A > B")
            return 1
        elif "B" in odpowiedz_clean:
            print("B > A")
            return 0
        else:
            print("niejednoznacznie")
            score_a = -co1_values[0] + co1_values[1] + co1_values[2]
            score_b = -co2_values[0] + co2_values[1] + co2_values[2]
            return 1 if score_a >= score_b else 0


