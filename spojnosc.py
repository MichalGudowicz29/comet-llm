import numpy as np
from pymcdm.methods.comet_tools import triads_consistency
import csv 
import sys


if len(sys.argv) != 2:
    print("Usage: python spojnosc.py <file_name>")
    sys.exit(1)

file_name = sys.argv[1]

with open(file_name, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

mej = np.array(data, dtype=float)


print(triads_consistency(mej))