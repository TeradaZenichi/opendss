## Scrip para casmento entre das datas entre os arquivos de geração PV e das cargas

import pandas as pd
import os
import datetime



dir_datasets = 'datasets/'

# Diretório de arquivos de geração PV
dir_pv = 'datasets/generation_profiles/'

# Diretório de arquivos de cargas
dir_cargas = 'datasets/load_profiles/'

# Preenchendo das 20:00 até 5:15 do outro dia com 0 as potências de geração PV
# Carregar o arquivo CSV
file_path = dir_pv + 'dados_completados.csv'  # Substitua pelo caminho do seu arquivo
data = pd.read_csv(file_path)

# Converter a coluna 'DateTime' para datetime
data['datetime'] = pd.to_datetime(data['datetime'])

# Identificar o menor ano no dataset
min_date = data['datetime'].min()
print("Data mínima:", min_date)

max_date = data['datetime'].max()
print("Data mínima:", min_date)

# Criar um range de datas começando em min_date e terminadno em max_date com um offset de 7 anos a menos e timestep de 15 minutos
date_range = pd.date_range(start=min_date - pd.DateOffset(years=7), end=max_date- pd.DateOffset(years=7), freq='15min')

data['datetime'] = data['datetime'] - pd.DateOffset(years=7)

data_power = data[['datetime', 'power']]

#Salva o novo dataframe
data_power.to_csv(dir_pv + 'dados_power_ajustado.csv', index=False)


