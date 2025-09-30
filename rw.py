import numpy as np
import pymcdm as pm
import matplotlib.pyplot as plt
from pymcdm.helpers import correlation_matrix
from pymcdm.correlations import rw

rankings = np.array([
    [5, 6, 1, 7, 8, 3, 4, 2], #run1
    [6, 5, 1, 7, 8, 3, 2, 4], #run2
    [5, 6, 1, 8, 7, 3, 4, 2]  # run3
])

# Oblicz macierz korelacji RW między wszystkimi parami
corr_matrix = correlation_matrix(rankings, rw)

labels = ['Run 1', 'Run 2', 'Run 3']

pm.visuals.correlation_heatmap(
    corr_matrix, 
    labels=labels,
    colorbar=True,
    cmap='Greens'
)

plt.show()
plt.savefig('correlation_heatmap_rw_temp0.5.png')
