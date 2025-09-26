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
        [249, 2, 1.6, 32, 1.42, 14.0],    # Lenovo IdeaPad 100S-14IBR budzetowy
        [544, 4, 2.0, 1000, 2.23, 15.6],  # Acer Aspire E5-576G srednia polka 
        [1869, 8, 1.6, 256, 1.23, 13.3],  # Dell XPS 13 ultrabook
        [1199, 8, 2.5, 256, 2.4, 15.6],   #  GL62M 7RD gaming
        [2250.68, 8, 2.3, 256, 2.04, 15.6], # Dell XPS 15 laptop do pracy
        [2799, 32, 2.7, 512, 3.8, 17.3]   # Asus ROG G701VI gaming high-end
    ]

    model_id = "llama3.1:8b"
    
    print("ALTERNATYWY:")
    alt_text = ""
    for i, alt in enumerate(alternatives):
        alt_text += (f"{i+1}. Price ={alt[0]}, RAM size={alt[1]}, "
                    f"CPU freq={alt[2]}, Storage in gb={alt[3]}, "
                    f"weight in kg={alt[4]}, screen size in inches={alt[5]}\n")

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
