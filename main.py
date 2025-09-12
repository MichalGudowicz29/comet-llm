import numpy as np
from pymcdm.methods import COMET
from llm_expert import LLMExpert


def main():
    print("COMET z LLM Expert")
    
    # 1. Definicja wartości charakterystycznych (cvalues)
    # Dla każdego kryterium definiujemy 3 poziomy (min, średni, max)
    cvalues = [
        [1, 5, 10],    # Kryterium 1: np. cena (niższa lepsza)
        [2, 6, 10],    # Kryterium 2: np. jakość (wyższa lepsza)
        [0, 5, 10]     # Kryterium 3: np. dostępność (wyższa lepsza)
    ]
    
    print("Wartości charakterystyczne:")
    for i, cv in enumerate(cvalues):
        print(f"  Kryterium {i+1}: {cv}")
    
    # Obliczamy liczbę obiektów charakterystycznych i porównań
    n_objects = np.prod([len(cv) for cv in cvalues])
    n_comparisons = n_objects * (n_objects - 1) // 2
    
    print(f"\nObiekty charakterystyczne: {n_objects}")
    print(f"Porównania parowe: {n_comparisons}")
    print("\nUWAGA: To może zająć trochę czasu!")
    
    # 2. ID modelu
    model_id = "llama3.2:3b"  # Pobierz z http://127.0.0.1:1234/v1/models lub ollama list 
    print(f"Używany model: {model_id}")
    
    # 3. Tworzenie eksperta LLM (zamiast ManualExpert)
    expert_function = LLMExpert(model_id, criteria_names=["cost","quality","avaliblity"])
    
    # 4. Utworzenie modelu COMET
    comet = COMET(cvalues, expert_function)
    print("Model COMET utworzony")
    
    # 5. Ocena alternatyw
    # alternatives = [
    #     [3, 8, 7],   # Średnia cena, dobra jakość, dobra dostępność
    #     [8, 4, 9],   # Wysoka cena, słaba jakość, bardzo dobra dostępność
    #     [6, 6, 6]    # Średnie wszystko
    # ]

    # obvious test 
    alternatives = [
        [10, 2, 0],  # NAJGORSZE: najdroższe, najgorsza jakość, niedostępne
        [5, 6, 5],   # ŚREDNIE: średnia cena, średnia jakość, średnia dostępność  
        [1, 10, 10]  # NAJLEPSZE: najtańsze, najlepsza jakość, w pełni dostępne
    ]
    
    print(f"\nAlternatywy do oceny:")
    for i, alt in enumerate(alternatives):
        print(f"  Alternatywa {i+1}: {alt}")
    
    print("\nOcenianie alternatyw...")
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

