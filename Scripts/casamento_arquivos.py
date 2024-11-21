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

# # Carregar o arquivo CSV
# file_path = dir_pv + 'dados_completados.csv' 
# data = pd.read_csv(file_path)

# # Converter a coluna 'DateTime' para datetime
# data['datetime'] = pd.to_datetime(data['datetime'])

# # Identificar o menor ano no dataset
# min_date = data['datetime'].min()
# print("Data mínima:", min_date)

# max_date = data['datetime'].max()
# print("Data mínima:", min_date)

# # Criar um range de datas começando em min_date e terminadno em max_date com um offset de 7 anos a menos e timestep de 15 minutos
# date_range = pd.date_range(start=min_date - pd.DateOffset(years=7), end=max_date- pd.DateOffset(years=7), freq='15min')

# data['datetime'] = data['datetime'] - pd.DateOffset(years=7)

# data_power = data[['datetime', 'power']]

# #Salva o novo dataframe
# data_power.to_csv(dir_pv + 'dados_power_ajustado.csv', index=False)

# Trocando os nomes das colunas para manter um mesmo padrão
# Dicionário com os nomes antigos e novos das colunas
renomear_colunas = {
    'LCLid': 'id',
    'DateTime': 'datetime',
    'KWH/hh (per half hour) ': 'power',
    # Adicione mais pares conforme necessário
}

# Iterar sobre os arquivos no diretório
for arquivo in os.listdir(dir_cargas):
    if arquivo.endswith('.csv'):  # Filtrar apenas arquivos .csv
        caminho_arquivo = os.path.join(dir_cargas, arquivo)

        # Carregar o arquivo CSV
        try:
            df = pd.read_csv(caminho_arquivo)

            # Renomear as colunas
            df.rename(columns=renomear_colunas, inplace=True)

            # Salvar o arquivo com o mesmo nome (substituir o original)
            df.to_csv(caminho_arquivo, index=False)
            print(f"Arquivo processado: {arquivo}")
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
