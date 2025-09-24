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
    comet_ranking = [1,3,2,7,4,8,5,9,6] # Tutaj wpisac ranking ktory dal nam nasz main.py 
    print(f"Ranking COMET: {comet_ranking}")
    
    # 3. Porównanie
    print(f"\n--- PORÓWNANIE ---")
    print(f"LLM:   {llm_ranking}")
    print(f"COMET: {comet_ranking}")


if __name__ == "__main__":
    compare_rankings()
