## Scrip para casmento entre das datas entre os arquivos de geração PV e das cargas

import pandas as pd
import os


dir_datasets = 'datasets/'

# Diretório de arquivos de geração PV
dir_pv = 'datasets/generation_profiles/'

# Diretório de arquivos de cargas
dir_cargas = 'datasets/load_profiles/'


# Verificação das datas iniciais e finais dos arquivos de carga

# Lista de arquivos de cargas
arquivos_cargas = os.listdir(dir_cargas)

for file in arquivos_cargas:
    df = pd.read_csv(dir_cargas + file)
    print(file)
    print(df['datetime'].min())
    print(df['datetime'].max())
    print('----------------------')


