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

        # Wybierz sugestie
        #goal = "None, just pick the best laptop overall."
        #goal = "Find the best laptop for gaming."
        #goal = "Find the most budget-friendly laptop for everyday tasks."
        #goal = "Find the best laptop for work."
        #goal = "Find the best laptop for programming and software development."
        #DONE log_laptopy_travel_od_nowa###goal = "Find the lightest, most compact laptop suitable for frequent travel."
        #goal = "Find the best laptop for graphic design and video editing."
        #goal = "Find the best laptop for a mix of gaming and work."
        #goal = "Find the best laptop for students on a budget."
        #goal = "Find the best laptop for business professionals."
        #goal = "Find the best laptop for casual use and media consumption."
        #DONE log_laptopy_cheapest.txt##goal = "Find the absolute cheapest laptop possible, regardless of performance."
        #goal = "Find the most powerful laptop for intensive computational tasks like AI training."
        goal = "None, just pick the best laptop overall."

        prompt = f"""
        You are choosing the optimal laptop.

BUSINESS GOAL: {goal}

Each alternative is a laptop with the following attributes:
- price in euros (lower is better if budget is important)
- RAM size in GB (higher is better if performance is important)
- CPU freq in GHz (higher is better for performance)
- storage type and size (larger capacity is better)
- weight in kg (lighter is better for portability)
- screen size in inches (smaller is better for mobility, larger is better for gaming and work)

Alternative A:
- price={co1_values[0]} euros
- RAM={co1_values[1]} GB
- cpu frequency={co1_values[2]} GHz
- storage={co1_values[3]} GB
- weight={co1_values[4]} kg
- screen size={co1_values[5]} inches
Alternative B:
- price={co2_values[0]} euros
- RAM={co2_values[1]} GB
- cpu frequency={co2_values[2]} GHz
- storage={co2_values[3]} GB 
- weight={co2_values[4]} kg
- screen size={co2_values[5]} inches

Think: Decide which laptop fits the goal better.  
Do not always pick based on price - interpret the goal and decide what matters most.  

Before choosing, answer:
- Which laptop better serves the goal?
- What specific advantages does each offer for goal?
Then choose based on goal requirements.

Answer only with "A" if alternative A is better, or "B" if alternative B is better  .
RESPOND WITH EXACTLY ONE CHARACTER: EITHER "A" OR "B"
NO EXPLANATIONS. NO ADDITIONAL TEXT. JUST THE LETTER.
"""

#         prompt = f"""
# You are choosing the optimal location for an EV charging station. 

# BUSINESS GOAL: Maximize the number of SHOPS nearby the potential station.

# CRITICAL RULE: 
# - The MAIN criterion is **shops**. 
# - The alternative with more shops MUST be chosen.


# Alternative A:
# - distance_parking={co1_values[0]}m   (lower is better)
# - distance_roads={co1_values[1]}m (lower is better)
# - distance_stations={co1_values[2]}m (lower is better)
# - shops={co1_values[3]} (higher is better)
# - restaurants={co1_values[4]} (higher is better) 
# - population_density={co1_values[5]} people nearby (higher is better)

# Alternative B: 
# - distance_parking={co2_values[0]}m  (lower is better)
# - distance_roads={co2_values[1]}m   (lower is better)  
# - distance_stations={co2_values[2]}m (lower is better)
# - shops={co2_values[3]} (higher is better)
# - restaurants={co2_values[4]} (higher is better)
# - population_density={co2_values[5]} people nearby  (higher is better)

# Think: The decision must be based PRIMARILY on SHOPS. 
# If one alternative has more shops, it should ALWAYS be chosen, even if other values are worse. 
# Only if shops are equal, then use the other factors as tie-breakers.

# Answer only with letter "A" if alternative A is better than alternative B or "B" when alternative B is better than alternative A do not explain or justify.
# """
 
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

