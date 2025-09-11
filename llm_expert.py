import numpy as np
from pymcdm.methods.comet_tools import ManualExpert
from llm import llm_query


class LLMExpert(ManualExpert):
    """
    klasa, która zastępuje ręczne odpowiedzi eksperta odpowiedziami LLM
    """
    
    def __init__(self, model_id: str):
        super().__init__()
        self.model_id = model_id
        self.pytanie_nr = 0
    
    def _query_user(self, co1: np.ndarray, co2: np.ndarray) -> int:
        """
        Metoda wywoływana przez COMET do porównania dwóch obiektów charakterystycznych.
        Zwraca 1 jeśli co1 > co2, 0 jeśli co1 < co2
        """
        self.pytanie_nr += 1
        print(f"\n--- Pytanie {self.pytanie_nr} ---")
        
        # Formatujemy obiekty charakterystyczne
        obiekt_a = f"Obiekt A: {co1}"
        obiekt_b = f"Obiekt B: {co2}"
        
        # Tworzymy prompt dla LLM
        prompt = f"""Porównaj dwa obiekty pod względem ich ogólnej jakości/atrakcyjności:

{obiekt_a}
{obiekt_b}

Który obiekt jest lepszy? Odpowiedz dokładnie "A" lub "B"."""

        print(f"Porównuję: {co1} vs {co2}")
        
        # Wysyłamy zapytanie do LLM
        odpowiedz = llm_query(prompt, self.model_id)
        print(f"Odpowiedź LLM: {odpowiedz}")
        
        # Parsujemy odpowiedź
        odpowiedz_clean = odpowiedz.strip().upper()
        
        if "A" in odpowiedz_clean:
            print("LLM wybrał A (co1 > co2)")
            return 1  # co1 jest lepszy
        else:
            print("LLM wybrał B (co2 > co1)")
            return 0  # co2 jest lepszy
