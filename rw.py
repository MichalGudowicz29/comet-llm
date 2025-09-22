import numpy as np
import pymcdm as pm
import matplotlib.pyplot as plt
from pymcdm.helpers import correlation_matrix
from pymcdm.correlations import rw

rankings = np.array([
    [1, 6, 9, 2, 8, 5, 3, 7, 4],  # LLM
    [1, 2, 3, 6, 5, 4, 9, 8, 7],  # COMET+LLM
    [3, 6, 9, 1, 2, 5, 4, 8, 7],  # LLM+Sugestie
    [1, 2, 3, 6, 4, 5, 9, 8, 7],  # COMET+LLM+Sugestie
])

# Oblicz macierz korelacji RW między wszystkimi parami
corr_matrix = correlation_matrix(rankings, rw)

labels = ['LLM', 'COMET+LLM', 'LLM+Sug.', 'COMET+LLM+Sug.']

pm.visuals.correlation_heatmap(
    corr_matrix, 
    labels=labels,
    colorbar=True,
    cmap='Greens'
)

plt.show()
