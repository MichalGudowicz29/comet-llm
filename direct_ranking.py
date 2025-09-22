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

    # alternatives = [
    #     [2, 9, 3],   # tanie, świetne, słabo dostępne
    #     [8, 4, 9],   # drogie, słabe, bardzo dostępne
    #     [4, 7, 6],   # średnio tanie, dobre, średnio dostępne
    #     [6, 6, 8],   # droższe, średnie, bardzo dostępne
    #     [3, 5, 5]    # tanie, średnie, średnie
    # ]

    alternatives = [
        #Dobre lokalizacja
        [120, 150, 1800, 40, 25, 50],   # Lok 1
        [200, 300, 1500, 35, 20, 45],   # Lok 2
        [250, 250, 1700, 30, 15, 40],   # Lok 3
        #Średnie lokalizacje 
        [500, 400, 1200, 20, 10, 25],   # Lok 4
        [600, 500, 1100, 18, 12, 22],   # Lok 5
        [450, 350, 1000, 15, 8, 20],    # Lok 6
        #Slabe lokalizacje 
        [800, 700, 500, 5, 3, 8],       # Lok 7
        [1000, 800, 400, 8, 4, 10],     # Lok 8
        [900, 900, 300, 6, 2, 12]       # Lok 9
    ]
    model_id = "llama3.2:3b"
    
    print("ALTERNATYWY:")
    alt_text = ""
    for i, alt in enumerate(alternatives):
        alt_text += (f"{i+1}. odległość_parking={alt[0]}, odległość_drogi={alt[1]}, "
                    f"odległość_stacje={alt[2]}, sklepy={alt[3]}, "
                    f"restauracje={alt[4]}, gęstość_zaludnienia={alt[5]}\n")

    print(alt_text)
        
    
    # 1. Bezpośredni LLM
    print(f"\n--- BEZPOŚREDNI LLM ---")
    llm_ranking = direct_llm_ranking(alternatives, model_id)
    print(f"Ranking LLM: {llm_ranking}")
    
    # 2. COMET+LLM  
    print(f"\n--- COMET+LLM ---") 
    comet_ranking = [1,2,3,6,4,5,9,8,7] # Tutaj wpisac ranking ktory dal nam nasz main.py 
    print(f"Ranking COMET: {comet_ranking}")
    
    # 3. Porównanie
    print(f"\n--- PORÓWNANIE ---")
    print(f"LLM:   {llm_ranking}")
    print(f"COMET: {comet_ranking}")


if __name__ == "__main__":
    compare_rankings()
