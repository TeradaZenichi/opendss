#Requireds libraries
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import opendssdirect as dss
from powerflow.bus import bus_dictionary
from powerflow.batery import distbess_dictionary
from powerflow.generators import distgen_dictionary,add_gd
from powerflow.get_powers import get_bus_power,display_branch_flows
from powerflow.load import add_LoadToBus,add_load
from powerflow.text_comands import set_frequency,new_circuit,line_geometry,add_line,add_infos


# Input and output directories

# Diretório de datasets
dir_datasets = 'C:\\Users\\joao9\\GitHub\\opendss\\datasets\\'

#Diretório de arquivos .dss
dir_dss = dir_datasets + 'arquivos_dss\\'

# Diretório de arquivos de geração PV
dir_pv = 'datasets\\generation_profiles\\'

# Diretório de arquivos de cargas
dir_cargas = 'datasets\\load_profiles\\'


# Initial definitions
Text = dss.Text
Circuit = dss.Circuit
Solution = dss.Solution

# Definições da MatPlotLib
plt.close('all')
plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (8,4)
plt.rcParams["figure.dpi"] = 100
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.sans-serif'] = ['cmr10']
plt.rcParams['axes.unicode_minus'] = False

#Potências máximas
PowerLoad=4
PowerPV=6 #Potência total dos módulos

# Definições do BESS
Pmin=0.320
BESS_P_MAX = 5
BESS_C_MAX = 12
SOC_MIN = 0.1 # 10%
SOC_MAX = 0.9 # 90%
BESS_E_MIN = BESS_C_MAX * SOC_MIN
BESS_E_MAX = BESS_C_MAX * SOC_MAX

# Definições do intervalo de simulação
# nconsumidores = len(os.listdir(dir_cargas))
nconsumidores = 3
nbarramentos = 4
horas = 24 #hours
intervalo = 30 #min

# Initializate the DSSFile
with open(dir_dss + 'ModelagemTeste.dss', 'w') as file:
    file.write(set_frequency(60) + '\n')
    file.write(new_circuit('ModelagemTeste', str(1).zfill(3), 0.22) + '\n')
    file.write(line_geometry(0.52,0.63,'km',3.338,3,3,[-120.00,0.00,60.00],[1000.00,1000.00,1000.00])+ '\n')
    for i in range(1,nbarramentos,1):
        file.write(add_line(i,str(i).zfill(3),str(i+1).zfill(3),25,'m',3)+ '\n')
    
    file.write(add_infos())

#Create the dicitonary of buses and loads in each bus
opendssmodel = dir_dss + 'ModelagemTeste.dss'

profiles = os.listdir(dir_cargas)

buses = bus_dictionary(nbarramentos)
for i in range(3):
    bus = 'bus_'+str(i+1).zfill(3)
    name = profiles[i].replace('.csv','')
    add_LoadToBus(buses,bus,name,2,0.22,1000,dir_cargas+profiles[i])

print(buses)


#Initiate the Power Flow

column_power = ['timestep', 'line', 'bus_1', 'bus_2', 'P', 'Q']
power_df = pd.DataFrame(columns = column_power)

#Descomentar quando for utilizar a função da Luíza

# column_node_power = ['timestep', 'name', 'P', 'Q', 'P_profile', 'Q_profile']
# node_power_df1 = pd.DataFrame(columns=column_node_power)

#Descomentar quando for utilizar a função do João
column_node_power = ['timestep', 'name', 'P', 'Q', 'V_a_b_c']
node_power_df1 = pd.DataFrame(columns=column_node_power)


range_time = pd.date_range('2012-07-06 12:00:00', periods=0.5*60/intervalo, freq=str(intervalo)+'T')
for time in range_time:

  dss.Basic.ClearAll()
  dss.Basic.Start(0)
  dss.Command(f"Compile {opendssmodel}")

  #Acessa os barramentos do dicionário
  for bus in buses.keys():
    loads = buses[bus].keys()
    for load in loads:
      carga = buses[bus][load]
      new_command = add_load(time,load,bus, carga['phases'],carga['voltage'], carga['profile'])
      dss.Command(new_command)
  
  dss.Solution.Solve()  # Solve the power flow
  # Display bus voltages
  voltages = dss.Circuit.AllBusVMag()
    
  print("\nBus Phase Voltages (V):")
  for bus, voltage in zip(buses.keys(), voltages):
      print(f"{bus}: {voltage:.4f}")

  # Display powers at buses
  total_activepower,total_reactivepower = get_bus_power(buses,dss)

  # Display power and current flows in branches
  display_branch_flows(dss)

  print("\nPower delivered to circuit:")
  print("Active power (kW)\tReactive power (kvar)")
  total_power = dss.Circuit.TotalPower()
  print(f"\t{total_power[0]:.4f}\t\t{total_power[1]:.4f}")
  print("\nTotal losses (kW): ")
  active_losses,reactive_losses = dss.Circuit.Losses()
  print(f"\t{active_losses / 1000:.4f}")

  print("\nPower Balance:")
  print("Active Power (kW)\tReactive Power (kvar)")
  print(f"\t{abs(total_power[0])-(total_activepower+active_losses/1000):.4f}\t\t{abs(total_power[1])-(total_reactivepower+reactive_losses/1000):.4f}")
