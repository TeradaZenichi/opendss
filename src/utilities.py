# File for utility functions

import pandas as pd

# Add loads in timestep i for a loop operation in OpenDSS
def add_load(i, name, bus, phases, kV, kW, profile, model=8, classe=1, vminpu=0.92, ZIPV=(0.5, 0, 0.5, 1, 0, 0, 0.5)):
  # Conectada em estrela
  new_load = f"New Load.{name} bus1={bus} Phases={phases} kV={kV} kW={kW*profile[0][i]:.2f} kVAr={kW*profile[1][i]:.2f} Model={model} Class={classe} Vminpu={vminpu} ZIPV={ZIPV}"

  return new_load

# Add generators in timestep i for a loop operation in OpenDSS
def add_gd(i, name, bus, phases, conn, kV, kW, profile, model=1, vminpu=0.92):
  new_gd = f"New Generator.{name} bus1={bus} Phases={phases} Conn={conn} kV={kV} kW={kW*profile[0][i]:.2f} kVAr={kW*profile[1][i]:.2f} Model={model} Vminpu={vminpu}"

  return new_gd

# Addd monitors in OpenDSS
def add_mon(monitors, element, terminal):
  new_mon = '\n\n'
  for i, name in enumerate(monitors):
    new_mon = new_mon + f"New Monitor.mon_{name}_vi element={element[i]} Terminal={terminal[i]} mode=0 ppolar=no\n"
    new_mon = new_mon + f"New Monitor.mon_{name}_pq element={element[i]} Terminal={terminal[i]} mode=1 ppolar=no\n"
  return new_mon

# New Monitor.mon_ipe_vi element=Transformer._oh_566670641_566670640_ Terminal=2 mode=0 ppolar=no
# New Monitor.mon_ipe_pq element=Transformer._oh_566670641_566670640_ Terminal=1 mode=1 ppolar=no


#Add a battery energy storage system in OpenDSS
def add_bess(i, name, bus, phases, conn, kV, kW, profile, model=1, vminpu=0.92):
  # print(i, name, bus, phases, conn, kV, kW, profile, model, vminpu)
  # Potência positiva: carrega,
  # Potência negativa: descarrega

  new_bess = f"New Load.{name} bus1={bus} Phases={phases} Conn={conn} kV={kV} kW={kW*profile[0][i]:.2f} kVAr={kW*profile[1][i]:.2f} Model={model} Vminpu={vminpu} "

  return new_bess

# Get the power flow in branchs 
def get_dist_power(column, i, power_df, loads, distgen, distbess):

  bus_to_search = []
  for load in loads:    bus_to_search.append([load, loads[load]['bus'].split('.', 1)[0], loads[load]['power']*loads[load]['profile'][0][i], loads[load]['power']*loads[load]['profile'][1][i]])
  for gen in distgen:   bus_to_search.append([gen,  distgen[gen]['bus'].split('.', 1)[0], distgen[gen]['power']*distgen[gen]['profile'][0][i], distgen[gen]['power']*distgen[gen]['profile'][1][i]])
  for bess in distbess: bus_to_search.append([bess, distbess[bess]['bus'].split('.', 1)[0], distbess[bess]['power']*distbess[bess]['profile'][0][i], distbess[bess]['power']*distbess[bess]['profile'][1][i]])

  # print(bus_to_search)

  node_power_df = pd.DataFrame(columns = column)

  for bus in bus_to_search:
      # Procurar os valores de potência dos barramentos das cargas e geração distribuída
      # print('bus')
      # print(bus[0], bus[1])

      flow_in  = power_df.index[power_df['bus_2'] == bus[1]].tolist()
      # print('flow in\n',flow_in)
      # Tratar flow in para ver se tem algum nó

      flow_out = power_df.index[power_df['bus_1'] == bus[1]].tolist()
      # print('flow out\n',flow_out)
      # Tratar flow out para ver se tem algum nó

      # print(flow_in, flow_out)
      P_in, P_out = 0, 0
      if (flow_in != []): P_in = power_df.loc[flow_in[-1], 'P']
      if (flow_out != []):P_out = power_df.loc[flow_out[0], 'P']
      P_node = P_in + P_out

      Q_in, Q_out = 0, 0
      if (flow_in != []): Q_in = power_df.loc[flow_in[-1], 'Q']
      if (flow_out != []):Q_out = power_df.loc[flow_out[0], 'Q']
      Q_node = Q_in + Q_out



      node_power_df = pd.concat([node_power_df, pd.DataFrame([[i, bus[0], P_node, Q_node, bus[2], bus[3]]], columns=column)])

      # print(bus[0], '// P: ', P_node, '// Q: ', Q_node)

  # display(node_power_df)
  return node_power_df


# Create a dictionary with the information of the loads
def load_dictionary(bus, phases, base_kv, base_power, dir_profile):
  load = {
          'bus': f"bus_{bus}.1.2.3",
          'phases': phases,
          'voltage': base_kv,
          'power': base_power,
          'profile': pd.read_csv(dir_profile,usecols=['datetime','power'])
      }
  return load

#Add a informations of the generator in a dictionary of generators
def distgen_dictionary(bus, phases, base_kv, base_power, dir_profile):
  distgen = {
          'bus': f"bus_{bus}.1.2.3",
          'phases': phases,
          'voltage': base_kv,
          'power': base_power,
          'profile': pd.read_csv(dir_profile,usecols=['datetime','power']),
          'conn': 'delta'
      }
  return distgen

#Add a informations of the battery energy storage system in a dictionary of bess
def distbess_dictionary(bus, phases, base_kv, base_power, dir_profile):
  distbess = {
          'bus': f"bus_{bus}.1.2.3",
          'phases': phases,
          'voltage': base_kv,
          'power': base_power,
          'profile': pd.read_csv(dir_profile,usecols=['datetime','power']),
          'conn': 'delta'
      }
  return distbess


##----------------- Funções para escrever o arquivo .dss -----------------##

#Set defaut frequency
def set_frequency(frequency):
  return f"Set DefaultBaseFrequency={frequency} \n"

#define the circuit
def new_circuit(name,bus,base_kv):
    new_comand = '!! Equivalente de Thèvenin \n'
    new_comand = new_comand + f"New Circuit.{name} bus1=bus_{bus}.1.2.3 basekV={base_kv} \n"

    return new_comand


#Define the cable specifications
def line_geometry(Rdc,Rac,Runits,Radius,Nconds,Nphases,X,H):
   new_comand = '!! Dados dos cabos e geometria das linhas\n'
   new_comand = new_comand + f"New WireData.Fios Rdc={Rdc} Rac={Rac} Runits={Runits} Radius={Radius} Radunits=mm \n"
   new_comand = new_comand + f"New LineSpacing.N1 Nconds={Nconds} Nphases={Nphases} Units=cm X=[{X[0]}  {X[1]}  {X[2]}] H=[ {H[0]}  {H[1]}  {H[2]}] \n"
   new_comand = new_comand + f"New LineGeometry.Geometria  Nconds={Nconds}  Spacing=N1 Wires=[Fios, Fios, Fios] Reduce=n' \n"

   return new_comand

def add_line(i,bus1, bus2, length, length_units, phases):
  if i==1:
    new_comand = '!! Linhas\n'
    new_comand = new_comand + f"New Line.Line_{bus1}_{bus2} Bus1=bus_{bus1} Bus2=bus_{bus2} Length={length} Units={length_units} Geometry=Geometria phases={phases}"
  else:
    new_comand = f"New Line.Line_{bus1}_{bus2} Bus1=bus_{bus1} Bus2=bus_{bus2} Length={length} Units={length_units} Geometry=Geometria phases={phases}"
  
  return new_comand 
    
def add_infos():
    new_command = """\
    
!! Outras informações
MakeBusList
Set VoltageBases = [.22]
CalcVoltageBases

Set maxiterations = 500
set mode=snap
!! Solve
"""
    return new_command



    