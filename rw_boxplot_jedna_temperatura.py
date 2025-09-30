import numpy as np
import pymcdm as pm
import matplotlib.pyplot as plt
from pymcdm.helpers import correlation_matrix
from pymcdm.correlations import rw
    
# Ranking referencyjny  COMET-LLM TEMP 0.0
reference = np.array([5, 6, 1, 8, 7, 3, 4, 2])

# Ranking CO referencyjny 
ranking_co = np.array([15., 5., 1., 18., 7., 2., 22., 12., 3., 16.5, 9., 4.,
20.5, 11., 6., 24., 13.5, 8., 25., 16.5, 10., 26., 20.5, 13.5,
27., 23., 19.])

## POROWNANIE Z RANKINGIEM REFERENCYJNYM ALTERNATYW

# Temperature 0.4
rankings_temp_0_4 = np.array([
    [5, 6, 1, 7, 8, 3, 2, 4],
    [5, 6, 1, 8, 7, 3, 2, 4],
    [5, 6, 1, 8, 7, 3, 4, 2],
    [5, 6, 1, 7, 8, 4, 3, 2],
    [5, 6, 1, 8, 7, 3, 2, 4],
    [5, 6, 1, 8, 7, 3, 2, 4],
    [6, 5, 1, 7, 8, 3, 2, 4],
    [5, 6, 1, 7, 8, 3, 4, 2],
    [5, 6, 1, 7, 8, 3, 4, 2],
    [6, 5, 1, 8, 7, 3, 2, 4]
])

# Oblicz RW dla temperatury 0.4
rw_temp_0_4 = np.zeros(len(rankings_temp_0_4))
for i in range(len(rankings_temp_0_4)):
    rw_temp_0_4[i] = rw(rankings_temp_0_4[i], reference)

print("RW dla temperatury 0.4:", rw_temp_0_4)



## POROWNANIE Z RANKINGIEM REFERENCYJNYM CO 
# Temperature 0.4
ranking_co_temp_0_4 = np.array([
    [9., 3.5, 2., 17.5, 6.5, 1., 19.5, 12.5, 6.5, 15., 8., 3.5,
22., 10.5, 5., 21., 10.5, 12.5, 26.5, 17.5, 15., 23.5, 25., 15.,
26.5, 23.5, 19.5], #run1
    [14., 7.5, 1., 17., 2., 3.5, 21.5, 9.5, 5.5, 19., 12., 5.5,
19., 7.5, 3.5, 24., 12., 9.5, 25.5, 16., 12., 25.5, 21.5, 15.,
27., 23., 19.], #run2
    [13.5, 3.5, 2., 13.5, 8., 1., 25., 17., 5., 19.5, 9.5, 6.,
19.5, 9.5, 3.5, 25., 17., 7., 23., 21., 13.5, 25., 11., 13.5,
27., 22., 17.], #run3
    [17., 5., 1.5, 13.5, 7., 1.5, 21., 13.5, 5., 21., 9.5, 5.,
17., 9.5, 3., 25., 15., 8., 23., 17., 11., 26., 21., 12.,
27., 24., 19.], #run4
    [15.5, 2.5, 1., 15.5, 7., 2.5, 24.5, 12., 6., 15.5, 9., 4.,
19., 8., 5., 27., 12., 10., 24.5, 18., 15.5, 23., 21.5, 12.,
26., 21.5, 20.], #run5
    [12.5, 5., 3., 15.5, 6., 2., 23., 12.5, 4., 20., 8., 1.,
23., 9.5, 7., 26., 18.5, 12.5, 23., 18.5, 9.5, 23., 15.5, 12.5,
27., 23., 17.], #run6
    [12.5, 3.5, 1., 10.5, 7., 2., 20., 12.5, 5.5, 15., 8.5, 5.5,
19., 15., 3.5, 24.5, 17.5, 10.5, 24.5, 17.5, 8.5, 26.5, 22., 15.,
26.5, 22., 22.], #run7
    [17., 5., 1., 20., 3.5, 2., 24., 12.5, 10.5, 20., 7., 3.5,
17., 10.5, 9., 22.5, 12.5, 7., 25.5, 15., 7., 25.5, 20., 17.,
27., 22.5, 14.], #run8
    [7., 3., 2., 14., 9., 1., 18., 13., 5., 23.5, 9., 5.,
18., 9., 5., 21., 18., 11.5, 23.5, 20., 11.5, 26., 23.5, 15.,
27., 23.5, 16.], #run9
    [17., 3.5, 1.5, 14.5, 9.5, 1.5, 23., 9.5, 8., 14.5, 6.5, 3.5,
21., 11.5, 5., 24.5, 17., 11.5, 26., 19., 6.5, 24.5, 17., 13.,
27., 21., 21.]  #run10
])

rw_co_temp_0_4 = np.zeros(len(ranking_co_temp_0_4))
for i in range(len(ranking_co_temp_0_4)):
    rw_co_temp_0_4[i] = rw(ranking_co_temp_0_4[i], ranking_co)

print("RW CO dla temperatury 0.4:", rw_co_temp_0_4)




# Macierze korelacji dla rankingów alternatyw
temperatures = [0.4]
rankings_data = [rankings_temp_0_4]

# Box plots dla korelacji z rankingiem referencyjnym alternatyw
rw_data = [rw_temp_0_4]

plt.figure(figsize=(12, 8))
plt.boxplot(rw_data, labels=[f'Temp {temp}' for temp in temperatures])
plt.xlabel('Temperature')
plt.ylabel('RW Correlation')
plt.title('RW Correlation with Reference Ranking (Alternatives)')
plt.grid(True, alpha=0.3)
plt.savefig('boxplot_rw_correlation_alternatives_S_R_N.png')
#plt.show()

# Macierze korelacji dla rankingów CO
rankings_co_data = [ranking_co_temp_0_4]

# Box plots dla korelacji z rankingiem referencyjnym CO
rw_co_data = [rw_co_temp_0_4]

plt.figure(figsize=(12, 8))
plt.boxplot(rw_co_data, labels=[f'Temp {temp}' for temp in temperatures])
plt.xlabel('Temperature')
plt.ylabel('RW Correlation')
plt.title('RW Correlation with Reference Ranking (CO)')
plt.grid(True, alpha=0.3)
plt.savefig('boxplot_rw_correlation_co_S_R_N.png')
#plt.show()
