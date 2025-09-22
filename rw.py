import numpy as np
import pymcdm as pm
import matplotlib.pyplot as plt

rankings = np.array([
    [1, 6, 9, 2, 8, 5, 3, 7, 4],  # LLM
    [1, 2, 3, 6, 5, 4, 9, 8, 7],  # COMET+LLM
    [3, 6, 9, 1, 2, 5, 4, 8, 7],  # LLM+Sugestie
    [1, 2, 3, 6, 4, 5, 9, 8, 7],  # COMET+LLM+Sugestie
])

# Oblicz macierz korelacji RW między wszystkimi parami
n = len(rankings)
corr_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i == j:
            corr_matrix[i, j] = 1.0  # Korelacja sama ze sobą = 1
        else:
            corr_matrix[i, j] = pm.correlations.rw(rankings[i], rankings[j])

labels = ['LLM', 'COMET+LLM', 'LLM+Sug.', 'COMET+LLM+Sug.']

pm.visuals.correlation_heatmap(
    corr_matrix, 
    labels=labels,
    colorbar=True,
    cmap='RdYlBu_r'
)

plt.show()
