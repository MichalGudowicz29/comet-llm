import numpy as np
import pymcdm as pm
import matplotlib.pyplot as plt
from pymcdm.helpers import correlation_matrix
from pymcdm.correlations import rw

rankings = np.array([
    [6, 4, 2, 3, 1, 5],  # LLM
    [3, 4, 6, 2, 5, 1],  # LLM+Sugestie
    [6, 5, 3, 4, 2, 1],  # COMET+LLM
    [6, 5, 3, 4, 2, 1],  # COMET+LLM+Sugestie
])

# Oblicz macierz korelacji RW między wszystkimi parami
corr_matrix = correlation_matrix(rankings, rw)

labels = ['LLM', 'LLM + S', 'COMET+L', 'COMET+L+S']

pm.visuals.correlation_heatmap(
    corr_matrix, 
    labels=labels,
    colorbar=True,
    cmap='Greens'
)

#plt.show()
plt.savefig('sugestia_preformance_rw.png', dpi=300)
