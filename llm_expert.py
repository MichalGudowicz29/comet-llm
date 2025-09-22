import numpy as np
from manual_expert import ManualExpert
from triad_supported_expert import TriadSupportExpert
from llm import llm_query
import re

# TriadSupport zamiast ManualExpert zeby zaoszczedzic czas 
class LLMExpert(TriadSupportExpert):
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
You are an expert in multi-criteria decision making.  
Two alternatives (A and B) are described by the same set of criteria.  

Criteria: distance_parking, distance_roads, distance_stations, shops, restaurants, population_density  

Alternative A: distance_parking={co1_values[0]}, distance_roads={co1_values[1]}, distance_stations={co1_values[2]}, shops={co1_values[3]}, restaurants={co1_values[4]}, population_density={co1_values[5]}  

Alternative B: distance_parking={co2_values[0]}, distance_roads={co2_values[1]}, distance_stations={co2_values[2]}, shops={co2_values[3]}, restaurants={co2_values[4]}, population_density={co2_values[5]}  

Your task: decide which alternative is better overall.  
Answer with **only one letter: A or B**. Do not explain, justify, or add anything else.  

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

