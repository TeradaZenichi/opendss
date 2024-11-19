## Scrip para casmento entre das datas entre os arquivos de geração PV e das cargas

import pandas as pd
import os


dir_datasets = 'datasets/'

# Diretório de arquivos de geração PV
dir_pv = 'datasets/generation_profiles/'

# Diretório de arquivos de cargas
dir_cargas = 'datasets/load_profiles/'

# Preenchendo das 20:00 até 5:15 do outro dia com 0 as potências de geração PV
# Carregar o arquivo CSV
file_path = dir_pv + 'df_unicamp_15m.csv'  # Substitua pelo caminho do seu arquivo
data = pd.read_csv(file_path,delimiter=';')

# Converter a coluna de data e hora (usar dayfirst=True para formatos DD/MM/YYYY)
data['datetime'] = pd.to_datetime(data['datetime'], dayfirst=True)

# Gerar um DataFrame vazio para preenchimento
rows_to_add = []

# Iterar por cada dia no DataFrame original
for day in data['datetime'].dt.date.unique():
    # Filtrar os registros do dia atual
    day_data = data[data['datetime'].dt.date == day]
    
    # Obter o horário inicial e final do dia
    start_time = day_data['datetime'].min()
    end_time = day_data['datetime'].max()
    
    # Verificar se há registros após as 20:00
    time_2000 = pd.Timestamp(day) + pd.Timedelta(hours=20)
    if end_time < time_2000:
        end_time = time_2000  # Garantir o final às 20:00
    
    # Criar registros de 20:15 até as 5:15 do próximo dia
    next_day = pd.Timestamp(day) + pd.Timedelta(days=1)
    fill_start = end_time + pd.Timedelta(minutes=15)
    fill_end = pd.Timestamp(next_day) + pd.Timedelta(hours=5, minutes=15)
    
    while fill_start <= fill_end:  # Incluindo o horário exato das 5:15
        rows_to_add.append({'datetime': fill_start, 'power': 0})
        fill_start += pd.Timedelta(minutes=15)

# Adicionar as novas linhas ao DataFrame
data = pd.concat([data, pd.DataFrame(rows_to_add)], ignore_index=True)

# Ordenar por data e hora
data = data.sort_values(by='datetime')

# Salvar o resultado em um novo arquivo
data.to_csv(dir_pv + 'dados_completados.csv', index=False)



