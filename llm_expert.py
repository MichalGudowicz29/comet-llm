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

## Prompt z Sugestia eksperta 
#         prompt = f"""
# You are an expert in multi-criteria decision making.  
# Two alternatives (A and B) are described by the same set of criteria.  

# Criteria: distance_to_parking_meters_lower_better, distance_to_roads_meters_lower_better, distance_to_charging_stations_meters_lower_better, number_of_nearby_shops_higher_better, number_of_nearby_restaurants_higher_better, population_density_higher_better

# Alternative A: distance_from_nearest_parking={co1_values[0]}, distance_from_nearest_roads={co1_values[1]}, distance_from_nearest_charging_stations={co1_values[2]}, amount of nearby shops={co1_values[3]}, amount of nearby restaurants={co1_values[4]}, amount of nearby population_density={co1_values[5]}  

# Alternative B: distance_from_nearest_parking={co2_values[0]}, distance_from_nearest_roads={co2_values[1]}, distance_from_nearest_charging_stations={co2_values[2]}, amount of nearby shops={co2_values[3]}, amount of nearby restaurants={co2_values[4]}, amount of nearby population_density={co2_values[5]}  

# Consider that our goal is to place NEW car chargers in place available to as many people as possible and to allow them to spend their free time while charging. Based on this goal, decide which criteria are more important and use this to determine the overall better alternative.  

# Your task: decide which alternative is better overall.  
# Answer with **only one letter: A or B**. Do not explain, justify, or add anything else.  

# """

# Prompt bez sugestii eksperta 
#         prompt = f"""
#         You are an expert in multi-criteria decision making.  
# Two alternatives (A and B) are described by the same set of criteria.  

# Criteria: distance_parking, distance_roads, distance_stations, shops, restaurants, population_density  

# Alternative A: distance_parking={co1_values[0]}, distance_roads={co1_values[1]}, distance_stations={co1_values[2]}, shops={co1_values[3]}, restaurants={co1_values[4]}, population_density={co1_values[5]}  

# Alternative B: distance_parking={co2_values[0]}, distance_roads={co2_values[1]}, distance_stations={co2_values[2]}, shops={co2_values[3]}, restaurants={co2_values[4]}, population_density={co2_values[5]}  

# Your task: decide which alternative is better overall.  
# Answer with **only one letter: A or B**. Do not explain, justify, or add anything else.  
#         """


        # Poprawiony prompt bazowy bez sugestii eksperta
        prompt = f"""
        You are evaluating locations for electric vehicle charging stations using multi-criteria decision analysis.

Two location alternatives (A and B) are characterized by:
- distance_parking: distance to nearest parking (meters)
- distance_roads: distance to main roads (meters) 
- distance_stations: distance to existing charging stations (meters)
- shops: number of nearby shops within 500m
- restaurants: number of nearby restaurants within 500m
- population_density: people per km²

# Alternative A: distance_parking={co1_values[0]}, distance_roads={co1_values[1]}, distance_stations={co1_values[2]}, shops={co1_values[3]}, restaurants={co1_values[4]}, population_density={co1_values[5]}  

# Alternative B: distance_parking={co2_values[0]}, distance_roads={co2_values[1]}, distance_stations={co2_values[2]}, shops={co2_values[3]}, restaurants={co2_values[4]}, population_density={co2_values[5]}  

Choose the better location overall. Answer with only: A or B
        """

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

