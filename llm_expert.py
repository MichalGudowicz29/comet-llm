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
#Test
        prompt = f"""
You are choosing the optimal location for an EV charging station. 

BUSINESS GOAL: Maximize the number of people who will use this charging station.

Alternative A:
- distance_parking={co1_values[0]}m   (lower is better)
- distance_roads={co1_values[1]}m (lower is better)
- distance_stations={co1_values[2]}m (lower is better)
- shops={co1_values[3]} (higher is better)
- restaurants={co1_values[4]} (higher is better) 
- population_density={co1_values[5]} people nearby (higher is better)

Alternative B: 
- distance_parking={co2_values[0]}m  (lower is better)
- distance_roads={co2_values[1]}m   (lower is better)  
- distance_stations={co2_values[2]}m (lower is better)
- shops={co2_values[3]} (higher is better)
- restaurants={co2_values[4]} (higher is better)
- population_density={co2_values[5]} people nearby  (higher is better)

Think: Which location will serve MORE PEOPLE? Choose the location that maximizes potential users.

Answer only with letter "A" if alternative A is better than alternative B or "B" when alternative B is better than alternative A do not explain or justify.
"""
        # Poprawiony prompt bazowy bez sugestii eksperta
#         prompt = f"""
#         You are evaluating locations for electric vehicle charging stations using multi-criteria decision analysis.

# Two location alternatives (A and B) are characterized by:
# - distance_parking: distance to nearest parking (meters)
# - distance_roads: distance to main roads (meters) 
# - distance_stations: distance to existing charging stations (meters)
# - shops: number of nearby shops within 500m
# - restaurants: number of nearby restaurants within 500m
# - population_density: number of residental houses within 500m

# # Alternative A: distance_parking={co1_values[0]}, distance_roads={co1_values[1]}, distance_stations={co1_values[2]}, shops={co1_values[3]}, restaurants={co1_values[4]}, population_density={co1_values[5]}  

# # Alternative B: distance_parking={co2_values[0]}, distance_roads={co2_values[1]}, distance_stations={co2_values[2]}, shops={co2_values[3]}, restaurants={co2_values[4]}, population_density={co2_values[5]}  

# Choose the better location overall. Answer with only: A or B
#         """

        # Poprawiony prompt z sugestią eksperta
#         prompt = f"""
#         You are an EV charging station location expert. Goal: maximize station utilization and customer satisfaction.

# CRITERIA PRIORITIES for optimal EV charging locations:
# - distance_parking (m) → MINIMIZE (accessibility critical)
# - distance_roads (m) → MINIMIZE (visibility/traffic important)  
# - distance_stations (m) → BALANCE 1-3km (avoid cannibalization)
# - shops (count) → MAXIMIZE (charging convenience)
# - restaurants (count) → MAXIMIZE (customer experience)
# - population_density (people/km²) → MAXIMIZE (demand driver - highest priority)

# Alternative A: [values]
# Alternative B: [values]

# Consider: High population density locations with good accessibility and amenities perform best. Answer: A or B
#         """
        print(f"Porównuję: {co1_name} {co1_values} vs {co2_name} {co2_values}")

        odpowiedz = llm_query(prompt, self.model_id)
        odpowiedz_clean = odpowiedz.strip().upper()
        print(f"Prompt:\n{prompt}")
        print(f"RAW odpowiedź: '{odpowiedz}'")
        print(f"CLEAN odpowiedź: '{odpowiedz_clean}'")
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

