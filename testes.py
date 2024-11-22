# Add the src directory to the Python path
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from utilities import add_line,add_infos,line_geometry,set_frequency,new_circuit,distgen_dictionary,distbess_dictionary

# Diretório de datasets
dir_datasets = 'datasets/'

# Diretório de arquivos de geração PV
dir_pv = 'datasets/generation_profiles/'

# Diretório de arquivos de cargas
dir_cargas = 'datasets/load_profiles/'

print(set_frequency(60))
print(new_circuit('circuit_1', str(1).zfill(3), 0.22))
print(line_geometry(0.52,0.63,'km',3.338,3,3,[-120.00,0.00,60.00],[1000.00,1000.00,1000.00]))
for i in range(1,13,1):
    print(add_line(i,str(i).zfill(3),str(i+1).zfill(3),25,'m',3))

print(add_infos())


