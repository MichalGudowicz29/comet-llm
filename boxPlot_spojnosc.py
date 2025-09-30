import numpy as np
from pymcdm.methods.comet_tools import triads_consistency
import csv
import matplotlib.pyplot as plt

# Inicjalizacja list dla każdej temperatury
temp_0_0 = []
temp_0_2 = []
temp_0_4 = []
temp_0_6 = []
temp_0_8 = []
temp_1_0 = []

# Mapowanie zakresów plików do list
temperature_ranges = {
    (1, 10): temp_0_0,
    (11, 20): temp_0_2,
    (21, 30): temp_0_4,
    (31, 40): temp_0_6,
    (41, 50): temp_0_8,
    (51, 60): temp_1_0
}

# Przetwarzanie wszystkich 60 plików
for i in range(1, 61):
    file_name = f'spojnosc{i}.csv'
    
    try:
        # Wczytanie danych z pliku CSV
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        # Konwersja na array numpy
        mej = np.array(data, dtype=float)
        
        # Obliczenie triads_consistency
        consistency_value = triads_consistency(mej)
        
        # Przypisanie wyniku do odpowiedniej listy
        for (start, end), temp_list in temperature_ranges.items():
            if start <= i <= end:
                temp_list.append(consistency_value)
                print(f"Plik {file_name}: consistency = {consistency_value} -> {temp_list}")
                break
                
    except FileNotFoundError:
        print(f"Ostrzeżenie: Nie znaleziono pliku {file_name}")
    except Exception as e:
        print(f"Błąd przy przetwarzaniu pliku {file_name}: {e}")

# Wyświetlenie podsumowania
print("\n=== Podsumowanie ===")
print(f"Temperatura 0.0: {len(temp_0_0)} wartości")
print(f"Temperatura 0.2: {len(temp_0_2)} wartości")
print(f"Temperatura 0.4: {len(temp_0_4)} wartości")
print(f"Temperatura 0.6: {len(temp_0_6)} wartości")
print(f"Temperatura 0.8: {len(temp_0_8)} wartości")
print(f"Temperatura 1.0: {len(temp_1_0)} wartości")

# Przygotowanie danych do boxplota
data = [temp_0_0, temp_0_2, temp_0_4, temp_0_6, temp_0_8, temp_1_0]
temperatures = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

# Utworzenie boxplota
plt.figure(figsize=(12, 8))
plt.boxplot(data, tick_labels=[f'Temp {temp}' for temp in temperatures])
plt.xlabel('Temperature', fontsize=12)
plt.ylabel('Triads consistency', fontsize=12)
plt.title('Triads consistency among temperatures', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('boxplot_spojnosc.png', dpi=300)
print("\nBoxplot zapisany jako 'boxplot_spojnosc.png'")
plt.show()