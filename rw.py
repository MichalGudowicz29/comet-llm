import numpy as np
import pymcdm as pm
import matplotlib.pyplot as plt
from pymcdm.helpers import correlation_matrix
from pymcdm.correlations import rw

rankings = np.array([
    [3, 6, 8, 9, 2, 7, 4, 1, 5],  # LLM
    [1, 3, 2, 7, 4, 8, 5, 9, 6],  # COMET+LLM
    [3, 6, 8, 9, 2, 7, 4, 1, 5],  # LLM+Sugestie
    [1, 3, 2, 7, 5, 8, 4, 9, 6],  # COMET+LLM+Sugestie
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
