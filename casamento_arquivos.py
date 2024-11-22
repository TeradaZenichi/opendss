# Add the src directory to the Python path
import pandas as pd
import os
import sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Diretório de datasets
dir_datasets = 'datasets/'

# Diretório de arquivos de geração PV
dir_pv = 'datasets/generation_profiles/'

# Diretório de arquivos de cargas
dir_cargas = 'datasets/load_profiles/'

#Lista os arquivos no load_profiles
power = dir_pv + 'dados_power_normalizado.csv'

# Converte a coluna datetime para pd.datetime
data = pd.read_csv(power)
data['datetime'] = pd.to_datetime(data['datetime'])
data.to_csv(dir_pv + 'dados_power_normalizado.csv', index=False)



