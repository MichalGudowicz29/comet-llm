import numpy as np
import pymcdm as pm
import matplotlib.pyplot as plt
from pymcdm.helpers import correlation_matrix
from pymcdm.correlations import rw

rankings = np.array([
    [6, 4, 2, 3, 1, 5],  # LLM
    [1, 3, 2, 4, 5, 6],  # LLM+Sugestie
    [6, 5, 3, 4, 2, 1],  # COMET+LLM
    [1, 2, 4, 3, 5, 6]   # COMET+LLM+Sugestie
])

corr_matrix = correlation_matrix(rankings, rw)

labels = ['LLM', 'LLM + S', 'COMET+L', 'COMET+L+S']

pm.visuals.correlation_heatmap(
    corr_matrix, 
    labels=labels,
    colorbar=True,
    cmap='Greens'
)

#plt.show()
plt.savefig('sugestia_cheapest_rw.png', dpi=300)
