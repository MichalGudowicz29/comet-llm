from llm import llm_query, direct_llm_ranking
import numpy as np

def compare_rankings():
    """Porównuje COMET+LLM vs bezpośredni LLM"""
    
    # alternatives = [
    #     [10, 2, 0],  # NAJGORSZE 
    #     [5, 6, 5],   # ŚREDNIE
    #     [1, 10, 10]  # NAJLEPSZE
    # ]
    # Bardziej zbalansowne
    # alternatives = [
    #     [3, 8, 4],   # tanie, bardzo dobra jakość, słaba dostępność  
    #     [7, 5, 9],   # drogie, średnia jakość, świetna dostępność
    #     [5, 6, 6]    # średnie, średnie, średnie
    # ]

        alternatives = [
            [2, 9, 3],   # tanie, świetne, słabo dostępne
            [8, 4, 9],   # drogie, słabe, bardzo dostępne
            [4, 7, 6],   # średnio tanie, dobre, średnio dostępne
            [6, 6, 8],   # droższe, średnie, bardzo dostępne
            [3, 5, 5]    # tanie, średnie, średnie
        ]
    
    model_id = "llama3.2:3b"
    
    print("ALTERNATYWY:")
    for i, alt in enumerate(alternatives):
        print(f"  {i+1}. koszt={alt[0]}, jakość={alt[1]}, dostępność={alt[2]}")
    
    # 1. Bezpośredni LLM
    print(f"\n--- BEZPOŚREDNI LLM ---")
    llm_ranking = direct_llm_ranking(alternatives, model_id)
    print(f"Ranking LLM: {llm_ranking}")
    
    # 2. COMET+LLM  
    print(f"\n--- COMET+LLM ---") 
    comet_ranking = [4,2,3,5,1] # Tutaj wpisac ranking ktory dal nam nasz main.py 
    print(f"Ranking COMET: {comet_ranking}")
    
    # 3. Porównanie
    print(f"\n--- PORÓWNANIE ---")
    print(f"LLM:   {llm_ranking}")
    print(f"COMET: {comet_ranking}")


if __name__ == "__main__":
    compare_rankings()
<<<<<<< HEAD
=======

>>>>>>> 416b52b8702011743e1764b36929400a112c004e
