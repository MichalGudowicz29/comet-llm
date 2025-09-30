import numpy as np
import time
from pymcdm.methods import COMET
from llm_expert import LLMExpert


def main():
    # Pomiar czasu rozpoczęcia
    start_time = time.time()
    
    print("COMET z LLM Expert")
    
    # 1. Definicja wartości charakterystycznych (cvalues)
    # Dla każdego kryterium definiujemy 3 poziomy (min, średni, max)
    # cvalues = [
    #     [1, 5, 10],    # Kryterium 1: np. cena (niższa lepsza)
    #     [2, 6, 10],    # Kryterium 2: np. jakość (wyższa lepsza)
    #     [0, 5, 10]     # Kryterium 3: np. dostępność (wyższa lepsza)
    # ]

    # cvalues = [
    #     [1, 3, 5, 7, 10],    # koszt: 5 poziomów
    #     [2, 4, 6, 8, 10],    # jakość: 5 poziomów  
    #     [0, 3, 5, 7, 10]     # dostępność: 5 poziomów
    # ] 

    # # wartosci do ladowarek
    # cvalues = [
    #     [100, 500, 1000],      # 1. Odległość od parkingów (m) – MIN
    #     [100, 500, 1000],      # 2. Odległość od głównych dróg (m) – MIN
    #     [300, 1000, 2000],     # 3. Odległość do istniejących stacji (m) – MAX
    #     [5, 20, 40],           # 4. Ilość sklepów – MAX
    #     [2, 10, 25],           # 5. Ilość restauracji – MAX
    #     [10, 30, 60]           # 6. Gęstość zaludnienia (bloki) – MAX
    # ]


    # cvalues = [
    #     [200, 1000, 2800],        # 1. Cena (euro) – MIN
    #     [2, 8, 32],       # 2. RAM (GB) – MAX
    #     [1, 2, 3],      # 3. CPU freq (benchmark)
    #     # [32, 256, 1000],            # 4. Pojemność dysku (TB) – MAX
    #     # [1, 2, 4],          # 5. Waga (kg) – MIN
    #     # [13, 15, 18]       # 6. Rozmiar ekranu (cale) – MAX
    # ]

   # Wartosci do samochodow 
    cvalues = [
        [70, 110, 360], # C1: Mileage (k km) – MIN
        [35, 45, 70], # C2: Price (k PLN) – MIN
        [2013, 2017, 2018] # C3: Year – MAX
    ]

    
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
    
    # 3. Tworzenie eksperta LLM (zamiast ManualExpert)
#     - price in euros (lower is better if budget is important)
# - RAM size in GB (higher is better if performance is important)
# - CPU freq in GHz (higher is better for performance)
# - storage type and size (SSD is faster than HDD, larger capacity is better)
# - weight in kg (lighter is better for portability)
# - screen size in inches (smaller is better for mobility, larger is better for gaming and work)
    expert_function = LLMExpert(
        model_id, 
        criteria_names=[
            "mileage", 
            "price", 
            "year"
        ]
    )
    
    # 4. Utworzenie modelu COMET
    comet = COMET(cvalues, expert_function)
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
    
    print("\n Comet.p")
    preferences = comet(np.array(alternatives))
    print(comet.p)

    print("\n Ranking CO")
    print(comet.rank(comet.p))
    
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

    # Pomiar i wyświetlenie czasu wykonania
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n=== CZAS WYKONANIA ===")
    print(f"Całkowity czas procesu: {execution_time:.2f} sekund")
    print(f"Całkowity czas procesu: {execution_time/60:.2f} minut")


if __name__ == "__main__":
    main()

