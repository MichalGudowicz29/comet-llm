import numpy as np
from pymcdm.methods import COMET
from llm_expert import LLMExpert


def main():
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

    cvalues = [
        [20, 50, 120],        # 1. Odległość od parkingów (m) – MIN (krótsza = lepsza)
        [50, 100, 500],       # 2. Odległość od głównych dróg (m) – MIN
        [100, 250, 500],      # 3. Odległość do istniejących stacji (m) – MAX (większa = lepsza)
        [0, 2, 4],            # 4. Ilość sklepów – MAX
        [0, 5, 60],          # 5. Ilość restauracji – MAX
        [0, 250, 1100]       # 6. Gęstość zaludnienia – MAX
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
    model_id = "llama3.2:3b"  # Pobierz z http://127.0.0.1:1234/v1/models lub ollama list 
    print(f"Używany model: {model_id}")
    
    # 3. Tworzenie eksperta LLM (zamiast ManualExpert)
    expert_function = LLMExpert(
        model_id, 
        criteria_names=[
            "distance_parking", 
            "distance_roads", 
            "distance_stations", 
            "shops", 
            "restaurants", 
            "population_density"
        ]
    )
    
    # 4. Utworzenie modelu COMET
    comet = COMET(cvalues, expert_function)
    print("Model COMET utworzony")
    
    # 5. Ocena alternatyw
    # alternatives = [
    #     [3, 8, 7],   # Średnia cena, dobra jakość, dobra dostępność
    #     [8, 4, 9],   # Wysoka cena, słaba jakość, bardzo dobra dostępność
    #     [6, 6, 6]    # Średnie wszystko
    # ]

    # # obvious test 
    # alternatives = [
    #     [10, 2, 0],  # NAJGORSZE: najdroższe, najgorsza jakość, niedostępne
    #     [5, 6, 5],   # ŚREDNIE: średnia cena, średnia jakość, średnia dostępność  
    #     [1, 10, 10]  # NAJLEPSZE: najtańsze, najlepsza jakość, w pełni dostępne
    # ]

    # # Bardziej zbalansowne
    # alternatives = [
    #     [3, 8, 4],   # tanie, bardzo dobra jakość, słaba dostępność  
    #     [7, 5, 9],   # drogie, średnia jakość, świetna dostępność
    #     [5, 6, 6]    # średnie, średnie, średnie
    # ]

    # alternatives = [
    #     [2, 9, 3],   # tanie, świetne, słabo dostępne
    #     [8, 4, 9],   # drogie, słabe, bardzo dostępne
    #     [4, 7, 6],   # średnio tanie, dobre, średnio dostępne
    #     [6, 6, 8],   # droższe, średnie, bardzo dostępne
    #     [3, 5, 5]    # tanie, średnie, średnie
    # ]

    # alternatives = [
    #     #Dobre lokalizacja
    #     [120, 150, 1800, 40, 25, 50],   # Lok 1
    #     [200, 300, 1500, 35, 20, 45],   # Lok 2
    #     [250, 250, 1700, 30, 15, 40],   # Lok 3
    #     #Średnie lokalizacje 
    #     [500, 400, 1200, 20, 10, 25],   # Lok 4
    #     [600, 500, 1100, 18, 12, 22],   # Lok 5
    #     [450, 350, 1000, 15, 8, 20],    # Lok 6
    #     #Slabe lokalizacje 
    #     [800, 700, 500, 5, 3, 8],       # Lok 7
    #     [1000, 800, 400, 8, 4, 10],     # Lok 8
    #     [900, 900, 300, 6, 2, 12]       # Lok 9
    # ]

    #Faktyczne dane
    alternatives = [
        [27.0806445188686, 500, 500, 4, 57, 745],      # Lok 1
        [77.09176084680027, 74.79129720139595, 500, 4, 6, 208],   # Lok 2
        [63.30163608595961, 500, 500, 3, 0, 1081],     # Lok 3
        [30.384330931295878, 90.22181624382063, 500, 0, 3, 5],   # Lok 4
        [103.8554029820573, 500, 500, 2, 0, 68],       # Lok 5
        [14.69723652773175, 500, 500, 0, 0, 71],       # Lok 6
        [47.21723107, 500, 349.2442126166036, 2, 30, 206],   # Lok 7
        [45.55711931603732, 500, 204.54510904074675, 0, 6, 81],   # Lok 8
        [14.888901353082431, 500, 113.717469150257, 1, 5, 73]    # Lok 9
    ]




    print(f"\nAlternatywy do oceny:")
    for i, alt in enumerate(alternatives):
        print(f"  Alternatywa {i+1}: {alt}")
    
    preferences = comet(np.array(alternatives))
    
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

