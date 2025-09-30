import numpy as np
from pymcdm.methods import COMET, TOPSIS
from pymcdm.methods.comet_tools import MethodExpert
from llm_expert import LLMExpert


def main():
    print("COMET z LLM Expert")

   # Wartosci do samochodow 
    # cvalues = [
    #     [70, 110, 360], # C1: Mileage (k km) – MIN
    #     [35, 45, 70], # C2: Price (k PLN) – MIN
    #     [2013, 2017, 2018] # C3: Year – MAX
    # ]
    cvalues = [
        [70, 110, 360], # C1: Mileage (k km)
        [35, 45, 70], # C2: Price (k PLN)
        [2013, 2017, 2018] # C3: Year
    ]

    types = np.array([1, 1, -1])
    weights = np.array([1/3, 1/3, 1/3])

    
    print("Wartości charakterystyczne:")
    for i, cv in enumerate(cvalues):
        print(f"  Kryterium {i+1}: {cv}")
    
    # Obliczamy liczbę obiektów charakterystycznych i porównań
    n_objects = np.prod([len(cv) for cv in cvalues])
    n_comparisons = n_objects * (n_objects - 1) // 2
    
    print(f"\nObiekty charakterystyczne: {n_objects}")
    print(f"Porównania parowe: {n_comparisons}")
    
    # 2. ID modelu
    model_id = "llama3.1:8b"  # Pobierz z http://127.0.0.1:1234/v1/models lub ollama list 
    print(f"Używany model: {model_id}")
    
    expert_function = LLMExpert(
        model_id, 
        criteria_names=[
            "mileage", 
            "price", 
            "year"
        ]
    )
    
    # 4. Utworzenie modelu COMET
    comet = COMET(cvalues, MethodExpert(TOPSIS(), types=types, weights=weights))
    #comet = COMET(cvalues, expert_function)
    print("Model COMET utworzony")
    
    # 5. Ocena alternatyw

    alternatives = [
        [94.0, 69.9, 2017],   # A1
        [297.0, 42.0, 2013],  # A2
        [205.0, 68.9, 2015],  # A3
        [360.0, 36.9, 2014],  # A4
        [86.0, 59.9, 2017],   # A5
        [79.6, 63.8, 2017],   # A6
        [113.0, 56.9, 2015],  # A7
        [171.0, 58.0, 2016]   # A8
    ]



    print(f"\nAlternatywy do oceny:")
    for i, alt in enumerate(alternatives):
        print(f"  Alternatywa {i+1}: {alt}")
    
    preferences = comet(np.array(alternatives))
    print("\nComet.p")
    print(comet.p)

    print("\nRanking CO")
    print(comet.rank(comet.p))

    print("\nCOMET.co")
    print(comet)


    # 6. Wyniki
    print(f"\n=== WYNIKI ===")
    print("Preferencje (wyższe = lepsze):")
    for i, pref in enumerate(preferences):
        print(f"  Alternatywa {i+1}: {pref:.4f}")
    
    # Ranking
    ranking_indices = np.argsort(preferences)[::-1]  # Od najlepszej do najgorszej
    
    print(f"\nRanking (od najlepszej):")
    for i, idx in enumerate(ranking_indices):
        print(f"  {i+1}. Alternatywa {idx+1}: {alternatives[idx]} (score: {preferences[idx]:.4f})")

if __name__ == "__main__":
    main()

